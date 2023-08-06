from math import ceil
import numpy as np
from ..preproc.ccd_cuda import CudaFlatField, CudaLog
from ..preproc.shift import VerticalShift
from ..preproc.shift_cuda import CudaVerticalShift
from ..preproc.double_flatfield import DoubleFlatField
from ..preproc.double_flatfield_cuda import CudaDoubleFlatField
from ..preproc.phase_cuda import CudaPaganinPhaseRetrieval
from ..preproc.sinogram_cuda import CudaSinoProcessing
from ..preproc.sinogram import SinoProcessing
from ..misc.unsharp_cuda import CudaUnsharpMask
from ..reconstruction.fbp import Backprojector
from ..cuda.utils import get_cuda_context, __has_pycuda__, __pycuda_error_msg__, copy_big_gpuarray, replace_array_memory
from .fullfield import FullFieldPipeline

if __has_pycuda__:
    import pycuda.gpuarray as garray


class CudaFullFieldPipeline(FullFieldPipeline):
    """
    Cuda backend of FullFieldPipeline
    """

    FlatFieldClass = CudaFlatField
    DoubleFlatFieldClass = CudaDoubleFlatField
    PaganinPhaseRetrievalClass = CudaPaganinPhaseRetrieval
    UnsharpMaskClass = CudaUnsharpMask
    VerticalShiftClass = CudaVerticalShift
    SinoProcessingClass = CudaSinoProcessing
    MLogClass = CudaLog
    FBPClass = Backprojector

    def __init__(self, process_config, sub_region, logger=None, extra_options=None, cuda_options=None):
        self._init_cuda(cuda_options)
        super().__init__(
             process_config, sub_region,
             logger=logger, extra_options=extra_options
        )
        self._register_callbacks()


    def _init_cuda(self, cuda_options):
        if not(__has_pycuda__):
            raise ImportError(__pycuda_error_msg__)
        cuda_options = cuda_options or {}
        self.ctx = get_cuda_context(**cuda_options)
        self._d_radios = None
        self._d_sinos = None
        self._d_recs = None


    def _allocate_array(self, shape, dtype, name=None):
        d_name = "_d_" + name
        d_arr = getattr(self, d_name)
        if d_arr is None:
            self.logger.debug("Allocating %s: %s" % (name, str(shape)))
            d_arr = garray.zeros(shape, dtype)
            setattr(self, d_name, d_arr)
        return d_arr


    def _transfer_radios_to_gpu(self):
        self._allocate_array(self.radios.shape, "f", name="radios")
        self._d_radios.set(self.radios)
        self._h_radios = self.radios
        self.radios = self._d_radios

    def _process_finalize(self):
        self.radios = self._h_radios

    #
    # Callbacks
    #

    def _read_data_callback(self):
        self.logger.debug("Transfering radios to GPU")
        self._transfer_radios_to_gpu()

    def _rec_callback(self):
        self.logger.debug("Getting reconstructions from GPU")
        self.recs = self.recs.get()

    def _saving_callback(self):
        self.recs = self._d_recs
        self.radios = self._h_radios


    def _register_callbacks(self):
        self.register_callback("read_chunk", self._read_data_callback)
        if self.reconstruction is not None:
            self.register_callback("reconstruction", self._rec_callback)
        if self.writer is not None:
            self.register_callback("save", self._saving_callback)




class CudaFullFieldPipelineLimitedMemory(CudaFullFieldPipeline):
    """
    Cuda backend of FullFieldPipeline, adapted to the case where not all the
    images fit in device memory.

    The classes acting on radios are not instantiated with the same shape as
    the classes acting on sinograms.
    """

    # In this case, the "build sinogram" step is best done on host to avoid
    # extraneous CPU<->GPU copies, and save some GPU memory.
    SinoProcessingClass = SinoProcessing
    # Same for DoubleFlatField
    DoubleFlatFieldClass = DoubleFlatField
    # VerticalShifts is simpler on host. It should be done on GPU if it slows down the process too much
    VerticalShiftClass = VerticalShift

    def __init__(self, process_config, sub_region, chunk_size, logger=None, extra_options=None, cuda_options=None):
        """
        Initialize a FullField pipeline with cuda backend, with limited memory
        setting.

        Important
        ----------
        The parameter `chunk_size` must be such that `chunk_size * Nx * Na` voxel
        can fit in device memory, especially when using Cuda/OpenCL.
        If not provided, `chunk_size` is equal to `delta_z = sub_region[-1] - sub_region[-2]`.
        So for wide detectors with a big number of radios, this is likely to fail.
        Providing a `chunk_size` accordingly enables to process the images by groups
        (see Notes below).
        This class always assumes that `delta_z * Nx * Na* fits in RAM (but not
        necessarily in GPU memory).


        Notes
        ------
        Let `Dz` be the subvolume height (i.e `sub_region[-1] - sub_region[-2]`),
        `Nx` the number of pixels horizontally, and `Na` the number of angles (radios),
        as illustrated below::


                     _________________
                    /                /|
                   /                / |
                  /________________/  |
                 |                 |  /
              Dz |                 | / Na
                 |_________________|/
                       Nx


        If the subvolume to process (`Dz * Nx * Na` voxels) is too big to fit in device memory,
        then images are processed by "groups" instead of processing the whole
        subvolume in one memory chunk.
        More precisely:
           - Radios are are processed by groups of `G` "vertical images"
             where `G` is such that `G * Dz * Nx` fits in memory
             (i.e `G * Dz * Nx = chunk_size * Nx * Na`)
           - Sinograms are processed by group of `chunk_size` "horizontal images"
             since by hypothesis `chunk_size * Nx * Na` fits in memory.
        """
        self._chunk_size = chunk_size
        super().__init__(
             process_config, sub_region,
             logger=logger, extra_options=extra_options,
             cuda_options=cuda_options
        )
        assert self.chunk_size < self.delta_z, "This class should be used when delta_z > chunk_size"
        # Internal limitation (make things easier)
        assert (self.delta_z % self.chunk_size) == 0, "delta_z must be a multiple of chunk_size"
        self._allocate_radios()
        self._h_recs = None
        self._old_flatfield = None
        # This is a current limitation.
        # Things are a bit tricky as chunk_size and delta_z would have to be
        # divided by binning_z, but then the group size has to be re-calculated.
        # On the other hand, it makes little sense to use this class
        # for other use cases than full-resolution reconstruction...
        if self.processing_options["read_chunk"]["binning"][-1] > 1:
            raise ValueError("Binning in z is not supported with this class")
        #


    def _init_reader_finalize(self):
        """
        Method called after _init_reader.
        In this case:
           - Reader gets all the data in memory (n_angles, delta_z, n_x)
           - CCD processing classes handle groups of images: (group_size, delta_z, n_x)
           - Sino processing classes handle stack of sinos (chunk_size, n_angles, n_x)
        """
        self.chunk_size = self._chunk_size
        n_a = self.dataset_infos.n_angles
        self.radios_group_size = (n_a * self.chunk_size) // self.delta_z
        self._n_radios_groups = ceil(n_a / self.radios_group_size)
        # (n_angles, delta_z, n_x) - fits in RAM but not in GPU memory
        self.radios = self.chunk_reader.files_data
        # (group_size, delta_z, n_x) - fits in GPU mem
        self.radios_group_shape = (self.radios_group_size, ) + self.radios.shape[1:]
        # passed to CCD processing classes
        self.radios_shape = self.radios_group_shape
        # DoubleFF is done on host. Here self.radios is still the host array (n_angles, delta_z, width)
        self._dff_radios_shape = self.radios.shape
        # Same for vertical shifts
        self._vshift_radios_shape = self.radios.shape
        if "flatfield" in self.processing_steps:
            # We need to update the projections indices passed to FlatField
            # for each group of radios
            ff_opts = self.processing_options["flatfield"]
            self._ff_proj_indices = ff_opts["projs_indices"]
            ff_opts["projs_indices"] = ff_opts["projs_indices"][:self.radios_group_size]
        # Processing acting on sinograms will be done later
        self._processing_steps = self.processing_steps.copy()
        for step in ["build_sino", "reconstruction", "save"]:
            self.processing_steps.remove(step)
        self._sinobuilder_radios_shape = (n_a, self.chunk_size, self.radios_shape[-1])


    def _allocate_radios(self):
        self._allocate_array(self.radios_group_shape, "f", name="radios")
        self._h_radios = self.radios # (n_angles, delta_z, width) (does not fit in GPU mem)
        self.radios = self._d_radios # (radios_group_size, delta_z, width) (fits in GPU mem)


    def _allocate_sinobuilder_output(self):
        self._allocate_array(self.sino_builder.output_shape, "f", name="sinos")
        self._h_sinos = np.zeros(self._d_sinos.shape, "f")
        self._sinobuilder_output = self._h_sinos # patch self.sino_builder
        return self._h_sinos

    def _allocate_recs(self, ny, nx):
        self.recs = self._allocate_array((self.chunk_size, ny, nx), "f", name="recs")


    def _register_callbacks(self):
        # No callbacks are registered for this subclass
        pass


    def _process_finalize(self):
        # release cuda memory
        replace_array_memory(self._d_sinos, (1,))
        self._d_sinos = None
        replace_array_memory(self._d_recs, (1,))
        self._d_recs = None
        # re-allocate _d_radios for processing a new chunk
        self.radios = self._h_radios
        self._allocate_radios()
        self.flatfield = self._old_flatfield


    def _reinit_flatfield(self, start_idx, end_idx, transfer_size):
        if "flatfield" in self.processing_steps:
            # We need to update the projections indices passed to FlatField
            # for each group of radios
            ff_opts = self.processing_options["flatfield"]
            ff_opts["projs_indices"] = self._ff_proj_indices[start_idx:end_idx]
            self._init_flatfield(shape=(transfer_size, ) + self.radios_shape[1:])


    def _flatfield_radios_group(self, start_idx, end_idx, transfer_size):
        self._reinit_flatfield(start_idx, end_idx, transfer_size)
        self._flatfield()


    def _apply_flatfield_and_dff(self, n_groups, group_size, n_images):
        """
        If double flat-field is activated, apply flat-field + double flat-field.
        Otherwise, do nothing and leave the flat-field for later "group processing"
        """
        if "double_flatfield" not in self.processing_steps:
            return
        for i in range(n_groups):
            self.logger.debug("processing group %d/%d" % (i+1, n_groups))
            start_idx = i * group_size
            end_idx = min((i + 1) * group_size, n_images)
            transfer_size = end_idx - start_idx
            # Copy H2D
            self._d_radios[:transfer_size, :, :] = self._h_radios[start_idx:end_idx, :, :]
            # Process a group of radios (radios_group_size, delta_z, width)
            self._old_radios = self.radios
            self.radios = self.radios[:transfer_size]
            self._flatfield_radios_group(start_idx, end_idx, transfer_size)
            self.radios = self._old_radios
            # Copy D2H
            self._d_radios[:transfer_size, :, :].get(ary=self._h_radios[start_idx:end_idx])
        # Here flat-field has been applied on all radios (n_angles, delta_z, n_x).
        # Now apply double FF on host.
        self._double_flatfield(radios=self._h_radios)
        if "flatfield" in self.processing_steps:
            self.processing_steps.remove("flatfield")
            self._old_flatfield = self.flatfield
            self.flatfield = None


    def _process_chunk_ccd(self):
        """
        Perform the processing in the "CCD space" (on radios)
        """
        n_groups = self._n_radios_groups
        group_size = self.radios_group_size
        n_images = self._h_radios.shape[0]

        self._apply_flatfield_and_dff(n_groups, group_size, n_images)

        for i in range(n_groups):
            self.logger.debug("processing group %d/%d" % (i+1, n_groups))
            start_idx = i * group_size
            end_idx = min((i + 1) * group_size, n_images)
            transfer_size = end_idx - start_idx
            # Copy H2D
            self._d_radios[:transfer_size, :, :] = self._h_radios[start_idx:end_idx, :, :]
            # Process a group of radios (radios_group_size, delta_z, width)
            self._old_radios = self.radios
            self.radios = self.radios[:transfer_size]
            self._flatfield_radios_group(start_idx, end_idx, transfer_size)
            self._retrieve_phase()
            self._apply_unsharp()
            self._take_log()
            self.radios = self._old_radios
            # Copy D2H
            self._d_radios[:transfer_size, :, :].get(ary=self._h_radios[start_idx:end_idx])
        self._radios_movements(radios=self._h_radios)
        self.logger.debug("End of processing steps on radios")

        # Restore original processing steps
        self.processing_steps = self._processing_steps
        # Initialize sino builder
        if "build_sino" in self.processing_steps:
            self._init_sino_builder()
            # release cuda memory of _d_radios if a new array was allocated for sinograms
            if self._sinobuilder_output is not None:
                replace_array_memory(self._d_radios, (1,))
                self._d_radios = None
            # otherwise use the buffer of _d_radios for _d_sinos
            else:
                self._d_sinos = garray.empty(
                    (self.chunk_size, ) + self.sino_builder.output_shape[1:],
                    "f",
                    gpudata=self._d_radios.gpudata
                )
                self._d_sinos.fill(0)


    def _process_chunk_sinos(self):
        """
        Perform the processing in the "sinograms space"
        """
        self.logger.debug("Initializing processing on sinos")
        self._prepare_reconstruction()
        self._init_reconstruction()
        self._init_writer()

        if self._h_recs is None:
            self._h_recs = np.zeros((self.delta_z, ) + self.recs.shape[1:], "f")

        n_groups = ceil(self.delta_z / self.chunk_size)
        group_size = self.chunk_size
        for i in range(n_groups):
            self.logger.debug("processing stack %d/%d" % (i+1, n_groups))
            start_idx = i * group_size
            end_idx = min((i + 1) * group_size, self.delta_z)
            transfer_size = end_idx - start_idx # not useful here as delta_z % chunk_size == 0
            # Build sinograms on host using _h_radios
            self._build_sino(radios=self._h_radios[:, start_idx:end_idx, :])
            # Copy H2D
            # pycuda does not support copy where "order" is not the same
            # (self.sinos might be a view on self.radios)
            if not(self._sinobuilder_copy) and not(self.sinos.flags["C_CONTIGUOUS"]):
                sinos = np.ascontiguousarray(self.sinos)
            else:
                sinos = self._h_sinos
            #
            self._d_sinos[:, :, :] = sinos[:, :, :]
            # Process stack of sinograms (chunk_size, n_angles, width)
            self._reconstruct(sinos=self._d_sinos)
            # Copy D2H
            self._d_recs.get(ary=self._h_recs[start_idx:end_idx])
        self.logger.debug("End of processing steps on sinos")
        # Write
        self._write_data(data=self._h_recs)


    def _process_chunk(self):
        self._process_chunk_ccd()
        self._process_chunk_sinos()
        self._process_finalize()

