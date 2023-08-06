from nabu.resources.dataset_analyzer import analyze_dataset
from nabu.io.reader import ChunkReader
from nabu.io.writer import NXProcessWriter
from nabu.preproc.ccd_cuda import CudaFlatField
from nabu.preproc.phase_cuda import CudaPaganinPhaseRetrieval
from nabu.preproc.ccd_cuda import CudaLog
from nabu.reconstruction.fbp import Backprojector
from nabu.cuda.utils import get_cuda_context
import pycuda.gpuarray as garray


class SimpleDataProcessor:
    def __init__(
        self, dataset_path, sub_region, rot_center=None, binning=None, delta_beta=100
    ):
        self.dataset_infos = analyze_dataset(dataset_path)
        self.sub_region = sub_region
        self.binning = binning
        self.rot_center = rot_center
        self.delta_beta = delta_beta
        self.dataset_path = dataset_path
        self._init_chunk_reader(sub_region)
        self._init_processing()

    def _init_chunk_reader(self, sub_region):
        self.chunk_reader = ChunkReader(
            self.dataset_infos.projections,
            sub_region=sub_region,
            pre_allocate=True,
            convert_float=True,
            binning=self.binning,
        )
        self.radios_np = self.chunk_reader.files_data
        n_a, n_z, n_x = self.radios_np.shape
        self.n_angles = n_a
        self.n_x = n_x
        self.n_z = n_z

    def _init_cuda(self):
        self.cuda_ctx = get_cuda_context()
        self.d_radios = garray.zeros(self.radios_np.shape, "f")
        self.d_recs = garray.zeros((self.n_z, self.n_x, self.n_x), "f")

    def _init_flatfield(self):
        # can be more elegant
        self.flatfield = CudaFlatField(
            self.radios_np.shape,
            self.dataset_infos.flats,
            self.dataset_infos.darks,
            radios_indices=sorted(self.dataset_infos.projections.keys()),
            cuda_options={"ctx": self.cuda_ctx},
            sub_region=self.sub_region,
            convert_float=True,
            binning=self.binning,
        )

    def _init_writer(self):
        self.rec_fname = self.dataset_path + str("_rec_%04d.hdf5" % self.sub_region[-2])
        self.writer = NXProcessWriter(self.rec_fname)

    def _init_processing(self):
        self._init_cuda()
        self._init_flatfield()
        energy = self.dataset_infos.energy
        # temp. fix
        if energy == 0:
            energy = 19.0  # keV
        #
        self.phase = CudaPaganinPhaseRetrieval(
            (self.n_z, self.n_x),
            distance=self.dataset_infos.distance * 1e2,
            energy=energy,
            delta_beta=self.delta_beta,
            pixel_size=self.dataset_infos.pixel_size,
            cuda_options={"ctx": self.cuda_ctx},
        )
        self.mlog = CudaLog(self.radios_np.shape)  # clip ?
        self.sinos_shape = (self.n_angles, self.n_x)
        self.fbp = Backprojector(
            self.sinos_shape,
            angles=self.dataset_infos.rotation_angles,
            rot_center=self.rot_center,
            extra_options={"padding_mode": "edges"},
            cuda_options={"ctx": self.cuda_ctx},
        )
        self._init_writer()

    def _reconfigure_chunk_reader(self):
        self.chunk_reader._set_subregion(self.sub_region)
        self.chunk_reader._init_reader()
        self.chunk_reader._loaded = False
        self.chunk_reader.files_data.fill(0)
        self._init_flatfield()
        self._init_writer()

    def _reset_sub_region(self, sub_region):
        dz0 = self.sub_region[-1] - self.sub_region[-2]
        dz = sub_region[-1] - sub_region[-2]
        if dz != dz0:
            raise ValueError(
                "Cannot change delta_z: was %d, requested %d. Please instantiate a new class"
                % (dz0, dz)
            )
        self.sub_region = sub_region
        self._reconfigure_chunk_reader()

    def process_data(self, sub_region=None):
        if sub_region is not None and sub_region != self.sub_region:
            self._reset_sub_region(sub_region)
        print("Loading %s" % str(self.sub_region))
        self.chunk_reader.load_files()
        print("Memcpy H2D")
        self.d_radios.set(self.radios_np)
        print("Flatfield")
        self.flatfield.normalize_radios(self.d_radios)
        print("Phase")
        for i in range(self.n_angles):
            self.phase.apply_filter(self.d_radios[i], output=self.d_radios[i])
        print("-log()")
        self.mlog.take_logarithm(self.d_radios)
        print("Reconstruction")
        for i in range(self.n_z):
            self.fbp.fbp(self.d_radios[:, i, :], output=self.d_recs[i])
        print("Memcpy D2H")
        recs = self.d_recs.get()
        print("Writing result to %s" % self.writer.fname)
        self.writer.write(recs, "reconstruction")  # todo config
