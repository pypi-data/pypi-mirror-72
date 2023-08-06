from os import path
import numpy as np
from ..resources.logger import LoggerOrPrint
from .utils import use_options, pipeline_step
from ..utils import check_supported
from ..io.reader import ChunkReader
from ..preproc.ccd import FlatField, Log
from ..preproc.shift import VerticalShift
from ..preproc.double_flatfield import DoubleFlatField
from ..preproc.phase import PaganinPhaseRetrieval
from ..preproc.sinogram import SinoProcessing
from ..misc.unsharp import UnsharpMask
from ..resources.utils import is_hdf5_extension
from ..io.writer import Writers

class FullFieldPipeline:
    """
    Pipeline for "regular" full-field tomography.
    Data is processed by chunks. A chunk consists in K contiguous lines of all the radios.
    In parallel geometry, a chunk of K radios lines gives K sinograms,
    and equivalently K reconstructed slices.
    """

    FlatFieldClass = FlatField
    DoubleFlatFieldClass = DoubleFlatField
    PaganinPhaseRetrievalClass = PaganinPhaseRetrieval
    UnsharpMaskClass = UnsharpMask
    VerticalShiftClass = VerticalShift
    SinoProcessingClass = SinoProcessing
    MLogClass = Log
    FBPClass = None # For now we don't have a plain python/numpy backend for reconstruction

    def __init__(self, process_config, sub_region, logger=None, extra_options=None):
        """
        Initialize a Full-Field pipeline.

        Parameters
        ----------
        processing_config: `nabu.resources.processcinfig.ProcessConfig`
            Process configuration.
        sub_region: tuple
            Sub-region to process in the volume for this worker, in the format
            `(start_x, end_x, start_z, end_z)`.
        logger: `nabu.app.logger.Logger`, optional
            Logger class
        extra_options: dict, optional
            Advanced extra options.
        """
        self.logger = LoggerOrPrint(logger)
        self._set_params(process_config, sub_region, extra_options)
        self.set_subregion(sub_region)
        self._init_pipeline()


    @staticmethod
    def _check_subregion(sub_region):
        if len(sub_region) < 4:
            assert len(sub_region) == 2
            sub_region = (None, None) + sub_region
        if None in sub_region[-2:]:
            raise ValueError("Cannot set z_min or z_max to None")
        return sub_region


    def _set_params(self, process_config, sub_region, extra_options):
        self.process_config = process_config
        self.dataset_infos = self.process_config.dataset_infos
        self.processing_steps = self.process_config.processing_steps
        self.processing_options = self.process_config.processing_options
        self.sub_region = self._check_subregion(sub_region)
        self.delta_z = sub_region[-1] - sub_region[-2]
        self.chunk_size = self.delta_z
        self._set_extra_options(extra_options)
        self._old_file_prefix = None
        self._callbacks = {}
        self._steps_name2component = {}
        self._steps_component2name = {}

    def _set_extra_options(self, extra_options):
        if extra_options is None:
            extra_options = {}
        advanced_options = {}
        advanced_options.update(extra_options)
        self.extra_options = advanced_options


    def set_subregion(self, sub_region):
        """
        Set a sub-region to process.

        Parameters
        ----------
        sub_region: tuple
            Sub-region to process in the volume, in the format
            `(start_x, end_x, start_z, end_z)` or `(start_z, end_z)`.
        """
        sub_region = self._check_subregion(sub_region)
        dz = sub_region[-1] - sub_region[-2]
        if dz != self.delta_z:
            raise ValueError(
                "Class was initialized for delta_z = %d but provided sub_region has delta_z = %d"
                % (self.delta_z, dz)
            )
        self.sub_region = sub_region
        self.z_min = sub_region[-2]
        self.z_max = sub_region[-1]


    def _get_process_name(self):
        # TODO support "incomplete" processing pipeline
        return "reconstruction"


    def register_callback(self, step_name, callback):
        """
        Register a callback for a pipeline processing step.

        Parameters
        ----------
        step_name: str
            processing step name
        callback: callable
            A function. It will be executed once the processing step `step_name`
            is finished. The function takes only one argument: the class instance.
        """
        if step_name not in self.processing_steps:
            raise ValueError(
                "'%s' is not in processing steps %s"
                % (step_name, self.processing_steps)
            )
        if step_name in self._callbacks:
            self.logger.warning("Overwriting existing callback for %s" % step_name)
        self._callbacks[step_name] = callback


    #
    # Class-specific
    #
    def _allocate_array(self, shape, dtype, name=None):
        return np.zeros(shape, dtype=dtype)


    def _reset_memory(self):
        pass


    def _init_reader_finalize(self):
        """
        Method called after _init_reader
        """
        self.radios = self.chunk_reader.files_data
        self.radios_shape = self.radios.shape
        self._sinobuilder_radios_shape = self.radios_shape
        self._dff_radios_shape = self.radios_shape
        self._vshift_radios_shape = self.radios.shape


    def _process_finalize(self):
        """
        Method called once the pipeline has been executed
        """
        pass

    #
    # Pipeline initialization
    #

    def _init_pipeline(self):
        self._init_reader()
        self._init_flatfield()
        self._init_double_flatfield()
        self._init_phase()
        self._init_unsharp()
        self._init_radios_movements()
        self._init_mlog()
        self._init_sino_builder()
        self._prepare_reconstruction()
        self._init_reconstruction()
        self._init_writer()

    @use_options("read_chunk", "chunk_reader")
    def _init_reader(self):
        if "read_chunk" not in self.processing_steps:
            raise ValueError("Cannot proceed without reading data")
        options = self.processing_options["read_chunk"]
        # ChunkReader always take a non-subsampled dictionary "files"
        self.chunk_reader = ChunkReader(
            options["files"],
            sub_region=self.sub_region,
            convert_float=True,
            binning=options["binning"],
            dataset_subsampling=options["dataset_subsampling"]
        )
        self._init_reader_finalize()

    @use_options("flatfield", "flatfield")
    def _init_flatfield(self, shape=None):
        if shape is None:
            shape = self.radios_shape
        options = self.processing_options["flatfield"]
        # FlatField parameter "radios_indices" must account for subsampling
        self.flatfield = self.FlatFieldClass(
            shape,
            flats=self.dataset_infos.flats,
            darks=self.dataset_infos.darks,
            radios_indices=options["projs_indices"],
            interpolation="linear",
            sub_region=self.sub_region,
            binning=options["binning"],
            convert_float=True
        )

    @use_options("double_flatfield", "double_flatfield")
    def _init_double_flatfield(self):
        options = self.processing_options["double_flatfield"]
        self.double_flatfield = self.DoubleFlatFieldClass(
            self._dff_radios_shape,
            result_url=None,
            input_is_mlog=False,
            output_is_mlog=False,
            average_is_on_log=False,
            sigma_filter=options["sigma"]
        )

    @use_options("phase", "phase_retrieval")
    def _init_phase(self):
        options = self.processing_options["phase"]
        # TODO pick phase retrieval method
        self.phase_retrieval = self.PaganinPhaseRetrievalClass(
            self.radios_shape[1:],
            distance=options["distance_cm"],
            energy=options["energy_kev"],
            delta_beta=options["delta_beta"],
            pixel_size=options["pixel_size_microns"],
            padding=options["padding_type"],
        )

    @use_options("unsharp_mask", "unsharp_mask")
    def _init_unsharp(self):
        options = self.processing_options["unsharp_mask"]
        self.unsharp_mask = self.UnsharpMaskClass(
            self.radios_shape[1:],
            options["unsharp_sigma"], options["unsharp_coeff"],
            mode="reflect", method="gaussian"
        )

    @use_options("take_log", "mlog")
    def _init_mlog(self):
        options = self.processing_options["take_log"]
        self.mlog = self.MLogClass(
            self.radios_shape,
            clip_min=options["log_min_clip"],
            clip_max=options["log_max_clip"]
        )

    @use_options("radios_movements", "radios_movements")
    def _init_radios_movements(self):
        options = self.processing_options["radios_movements"]
        self._vertical_shifts = options["translation_movements"][:, 1]
        self.radios_movements = self.VerticalShiftClass(
            self._vshift_radios_shape,
            self._vertical_shifts
        )

    @use_options("build_sino", "sino_builder")
    def _init_sino_builder(self):
        options = self.processing_options["build_sino"]
        self.sino_builder = self.SinoProcessingClass(
            radios_shape=self._sinobuilder_radios_shape,
            rot_center=options["rotation_axis_position"],
            halftomo=options["enable_halftomo"],
        )
        if not(options["enable_halftomo"]):
            self._sinobuilder_copy = False
            self._sinobuilder_output = None
            self.sinos = None
        else:
            self._sinobuilder_copy = True
            self.sinos = self._allocate_sinobuilder_output()
            self._sinobuilder_output = self.sinos

    def _allocate_sinobuilder_output(self):
        return self._allocate_array(self.sino_builder.output_shape, "f", name="sinos")


    @use_options("reconstruction", "reconstruction")
    def _prepare_reconstruction(self):
        options = self.processing_options["reconstruction"]
        x_s, x_e = options["start_x"], options["end_x"]+1
        y_s, y_e = options["start_y"], options["end_y"]+1
        self._rec_roi = (x_s, x_e, y_s, y_e)
        self.n_slices = self.radios_shape[1]  # TODO modify with vertical shifts
        self._allocate_recs(y_e - y_s, x_e - x_s)

    def _allocate_recs(self, ny, nx):
        self.recs = self._allocate_array((self.n_slices, ny, nx), "f", name="recs")


    @use_options("reconstruction", "reconstruction")
    def _init_reconstruction(self):
        options = self.processing_options["reconstruction"]
        # TODO account for reconstruction from already formed sinograms
        if self.sino_builder is None:
            raise ValueError("Reconstruction cannot be done without build_sino")
        else:
            sinos_shape = self.sino_builder.output_shape

        if options["enable_halftomo"]:
            rot_center = options["rotation_axis_position_halftomo"]
        else:
            rot_center = options["rotation_axis_position"]

        self.reconstruction = self.FBPClass(
            sinos_shape[1:],
            angles=options["angles"],
            rot_center=rot_center,
            filter_name=options["fbp_filter_type"],
            slice_roi=self._rec_roi,
            scale_factor=1./options["pixel_size_cm"],
            extra_options={
                "padding_mode": options["padding_type"],
                "axis_correction": options["axis_correction"],
            }
        )
        if options["fbp_filter_type"] == "none":
            self.reconstruction.fbp = self.reconstruction.backproj

    @use_options("save", "writer")
    def _init_writer(self):
        options = self.processing_options["save"]
        file_format = options["file_format"]
        if self._old_file_prefix is None:
            self._old_file_prefix = options["file_prefix"]
        options["file_prefix"] = self._old_file_prefix + "_%04d" % self.z_min

        check_supported(file_format, list(Writers.keys()), "output file format")
        self.fname = path.join(
            options["location"],
            options["file_prefix"] + "." + file_format
        )
        if path.exists(self.fname):
            err = "File already exists: %s" % self.fname
            if options["overwrite"]:
                if options.get("warn_overwrite", True):
                    self.logger.warning(err + ". It will be overwritten as requested in configuration")
                    options["warn_overwrite"] = False
            else:
                self.logger.fatal(err)
                raise ValueError(err)

        writer_cls = Writers[file_format]
        writer_args = [self.fname]
        writer_kwargs = {}
        self._writer_exec_args = []
        self._writer_exec_kwargs = {}
        if is_hdf5_extension(file_format):
            # ~ entry = str("entry%04" + self.z_min)
            entry = getattr(self.dataset_infos.dataset_scanner, "entry", None)
            nx_infos = {
                "process_name": self._get_process_name(),
                "processing_index": 0,
                "config": self.process_config.nabu_config,
                "entry": entry,
            }
            writer_kwargs["entry"] = nx_infos["entry"]
            writer_kwargs["filemode"] = "w" if options["overwrite"] else "a"
            self._writer_exec_args.append(nx_infos["process_name"])
            self._writer_exec_kwargs["processing_index"] = nx_infos["processing_index"]
            self._writer_exec_kwargs["config"] = nx_infos["config"]
        self.writer = writer_cls(*writer_args, **writer_kwargs)


    #
    # Pipeline re-initialization
    #

    def _reset_sub_region(self, sub_region):
        self.set_subregion(sub_region)
        # Reader
        self.chunk_reader._set_subregion(self.sub_region)
        self.chunk_reader._init_reader()
        self.chunk_reader._loaded = False
        # Flat-field
        if self.flatfield is not None:
            for reader in [self.flatfield.flats_reader, self.flatfield.darks_reader]:
                reader._set_subregion(self.sub_region)
                reader._init_reader()
                reader._loaded = False

    #
    # Pipeline execution
    #

    @pipeline_step("chunk_reader", "Reading data")
    def _read_data(self):
        self.logger.debug("Region = %s" % str(self.sub_region))
        self.chunk_reader.load_files()

    @pipeline_step("flatfield", "Applying flat-field")
    def _flatfield(self):
        self.flatfield.normalize_radios(self.radios)

    @pipeline_step("double_flatfield", "Applying double flat-field")
    def _double_flatfield(self, radios=None):
        if radios is None:
            radios = self.radios
        self.double_flatfield.apply_double_flatfield(radios)

    @pipeline_step("phase_retrieval", "Performing phase retrieval")
    def _retrieve_phase(self):
        for i in range(self.radios.shape[0]):
            self.phase_retrieval.apply_filter(self.radios[i], output=self.radios[i])

    @pipeline_step("unsharp_mask", "Performing unsharp mask")
    def _apply_unsharp(self):
        for i in range(self.radios.shape[0]):
            self.radios[i] = self.unsharp_mask.unsharp(self.radios[i])

    @pipeline_step("mlog", "Taking logarithm")
    def _take_log(self):
        self.mlog.take_logarithm(self.radios)


    @pipeline_step("radios_movements", "Applying radios movements")
    def _radios_movements(self, radios=None):
        if radios is None:
            radios = self.radios
        self.radios_movements.apply_vertical_shifts(
            radios, list(range(radios.shape[0]))
        )

    @pipeline_step("sino_builder", "Building sinograms")
    def _build_sino(self, radios=None):
        if radios is None:
            radios = self.radios
        # Either a new array (previously allocated in "_sinobuilder_output"),
        # or a view of "radios"
        self.sinos = self.sino_builder.radios_to_sinos(
            radios,
            output=self._sinobuilder_output,
            copy=self._sinobuilder_copy
        )

    @pipeline_step("reconstruction", "Reconstruction")
    def _reconstruct(self, sinos=None):
        if sinos is None:
            sinos = self.sinos
        for i in range(sinos.shape[0]):
            self.reconstruction.fbp(
                sinos[i], output=self.recs[i]
            )

    @pipeline_step("writer", "Saving data")
    def _write_data(self, data=None):
        if data is None:
            data = self.recs
        self.writer.write(data, *self._writer_exec_args, **self._writer_exec_kwargs)
        self.logger.info("Wrote %s" % self.writer.fname)


    def _process_chunk(self):
        self._flatfield()
        self._double_flatfield()
        self._retrieve_phase()
        self._apply_unsharp()
        self._take_log()
        self._radios_movements()
        self._build_sino()
        self._reconstruct()
        self._write_data()
        self._process_finalize()


    def process_chunk(self, sub_region=None):
        if sub_region is not None:
            self._reset_sub_region(sub_region)
            self._reset_memory()
            self._init_writer()
            self._init_double_flatfield()
        self._read_data()
        self._process_chunk()

