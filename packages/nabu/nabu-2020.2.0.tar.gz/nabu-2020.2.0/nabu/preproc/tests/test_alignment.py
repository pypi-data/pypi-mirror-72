import pytest
import numpy as np
import os
import h5py
from silx.third_party.EdfFile import EdfFile
try:
    import scipy.ndimage
    __has_scipy__ = True
except ImportError:
    __has_scipy__ = False

from nabu.preproc.alignment import CenterOfRotation, DetectorTranslationAlongBeam, AlignmentBase
from nabu.testutils import utilstest


@pytest.fixture(scope="class")
def bootstrap_base(request):
    cls = request.cls
    cls.abs_tol = 2.5e-2


@pytest.fixture(scope="class")
def bootstrap_cor(request):
    cls = request.cls
    cls.abs_tol = 0.2

    cls.data, cls.px = get_data_h5("tworadios.h5")


@pytest.fixture(scope="class")
def bootstrap_dtr(request):
    cls = request.cls
    cls.abs_tol = 1e-1

    # loading alignxc edf files from Christian. The last one is the dark. The first 6 are images for translation 0,1...6
    images = np.array([EdfFile(utilstest.getfile("alignxc%04d.edf" % i)).GetData(0, DataType="FloatValue") for i in range(7)])
    align_imgs, dark_img = images[:-1], images[-1]
    # removing dark
    cls.align_images = align_imgs - dark_img
    cls.img_pos = (1 + np.arange(6)) * 0.01

    cls.expected_shifts_vh = np.array((129.93, 353.18))

    cls.reference_shifts_list = [
        [0, 0],
        [-9.39, 11.29],
        [-5.02, 3.81],
        [-3.67, 9.73],
        [-4.72, 16.71],
        [6.02, 20.28],
    ]


def get_data_h5(*dataset_path):
    """
    Get a dataset file from silx.org/pub/nabu/data
    dataset_args is a list describing a nested folder structures, ex.
    ["path", "to", "my", "dataset.h5"]
    """
    dataset_relpath = os.path.join(*dataset_path)
    dataset_downloaded_path = utilstest.getfile(dataset_relpath)
    with h5py.File(dataset_downloaded_path, "r") as hf:
        nxentry = "entry/instrument/detector"
        px = hf[nxentry + "/x_rotation_axis_pixel_position"][()]
        data = hf[nxentry + "/data"][()]
    return data, px


@pytest.mark.usefixtures("bootstrap_base")
class TestAlignmentBase(object):
    def test_peak_fitting_2d_3x3(self):
        # Fit a 3 x 3 grid
        fy = np.linspace(-1, 1, 3)
        fx = np.linspace(-1, 1, 3)
        yy, xx = np.meshgrid(fy, fx, indexing="ij")

        peak_pos_yx = np.random.rand(2) * 1.6 - 0.8
        f_vals = np.exp(-((yy - peak_pos_yx[0]) ** 2 + (xx - peak_pos_yx[1]) ** 2) / 100)

        fitted_peak_pos_yx = AlignmentBase.refine_max_position_2d(f_vals, fy, fx)

        message = (
            "Computed peak position: (%f, %f) " % (*fitted_peak_pos_yx,)
            + " and real peak position (%f, %f) do not coincide." % (*peak_pos_yx,)
            + " Difference: (%f, %f)," % (*(fitted_peak_pos_yx - peak_pos_yx),)
            + " tolerance: %f" % self.abs_tol
        )
        assert np.all(np.isclose(peak_pos_yx, fitted_peak_pos_yx, atol=self.abs_tol)), message

    def test_peak_fitting_2d_error_checking(self):
        # Fit a 3 x 3 grid
        fy = np.linspace(-1, 1, 3)
        fx = np.linspace(-1, 1, 3)
        yy, xx = np.meshgrid(fy, fx, indexing="ij")

        peak_pos_yx = np.random.rand(2) + 1.5
        f_vals = np.exp(-((yy - peak_pos_yx[0]) ** 2 + (xx - peak_pos_yx[1]) ** 2) / 100)

        with pytest.raises(ValueError) as ex:
            AlignmentBase.refine_max_position_2d(f_vals, fy, fx)

        message = (
            "Error should have been raised about the peak being fitted outside margins, "
            + "other error raised instead:\n%s" % str(ex.value)
        )
        assert "positions are outide the input margins" in str(ex.value), message

    def test_extract_peak_regions_1d(self):
        img = np.random.randint(0, 10, size=(8, 8))

        peaks_pos = np.argmax(img, axis=-1)
        peaks_val = np.max(img, axis=-1)

        cc_coords = np.arange(0, 8)

        (found_peaks_val, found_peaks_pos) = AlignmentBase.extract_peak_regions_1d(img, axis=-1, cc_coords=cc_coords)
        message = "The found peak positions do not correspond to the expected peak positions:\n  Expected: %s\n  Found: %s" % (
            peaks_pos,
            found_peaks_pos[1, :],
        )
        assert np.all(peaks_val == found_peaks_val[1, :]), message


@pytest.mark.usefixtures("bootstrap_cor")
class TestCor(object):
    def test_cor_posx(self):
        radio1 = self.data[0, :, :]
        radio2 = np.fliplr(self.data[1, :, :])

        CoR_calc = CenterOfRotation()
        cor_position = CoR_calc.find_shift(radio1, radio2)

        message = "Computed CoR %f " % cor_position + " and real CoR %f do not coincide" % self.px
        assert np.abs(self.px - cor_position) < self.abs_tol, message

    def test_noisy_cor_posx(self):
        radio1 = np.fmax(self.data[0, :, :], 0)
        radio2 = np.fmax(self.data[1, :, :], 0)

        radio1 = np.random.poisson(radio1 * 400)
        radio2 = np.random.poisson(np.fliplr(radio2) * 400)

        CoR_calc = CenterOfRotation()
        cor_position = CoR_calc.find_shift(radio1, radio2, median_filt_shape=(3, 3))

        message = "Computed CoR %f " % cor_position + " and real CoR %f do not coincide" % self.px
        assert np.abs(self.px - cor_position) < self.abs_tol, message

    @pytest.mark.skipif(not(__has_scipy__), reason="need scipy for this test")
    def test_noisyHF_cor_posx(self):
        """  test with noise at high frequencies
        """
        radio1 = self.data[0, :, :]
        radio2 = np.fliplr(self.data[1, :, :])

        noise_level = radio1.max() / 16.0
        noise_ima1 = np.random.normal(0.0, size=radio1.shape) * noise_level
        noise_ima2 = np.random.normal(0.0, size=radio2.shape) * noise_level

        noise_ima1 = noise_ima1 - scipy.ndimage.filters.gaussian_filter(noise_ima1, 2.0)
        noise_ima2 = noise_ima2 - scipy.ndimage.filters.gaussian_filter(noise_ima2, 2.0)

        radio1 = radio1 + noise_ima1
        radio2 = radio2 + noise_ima2

        CoR_calc = CenterOfRotation()

        # cor_position = CoR_calc.find_shift(radio1, radio2)
        cor_position = CoR_calc.find_shift(radio1, radio2, low_pass=(6.0, 0.3))

        message = "Computed CoR %f " % cor_position + " and real CoR %f do not coincide" % self.px
        assert np.abs(self.px - cor_position) < self.abs_tol, message

    def test_cor_posx_linear(self):
        radio1 = self.data[0, :, :]
        radio2 = np.fliplr(self.data[1, :, :])

        CoR_calc = CenterOfRotation()
        cor_position = CoR_calc.find_shift(radio1, radio2, padding_mode="constant")

        message = "Computed CoR %f " % cor_position + " and real CoR %f do not coincide" % self.px
        assert np.abs(self.px - cor_position) < self.abs_tol, message

    def test_error_checking_001(self):
        CoR_calc = CenterOfRotation()

        radio1 = self.data[0, :, :1:]
        radio2 = self.data[1, :, :]

        with pytest.raises(ValueError) as ex:
            CoR_calc.find_shift(radio1, radio2)

        message = "Error should have been raised about img #1 shape, other error raised instead:\n%s" % str(ex.value)
        assert "Images need to be 2-dimensional. Shape of image #1" in str(ex.value), message

    def test_error_checking_002(self):
        CoR_calc = CenterOfRotation()

        radio1 = self.data[0, :, :]
        radio2 = self.data

        with pytest.raises(ValueError) as ex:
            CoR_calc.find_shift(radio1, radio2)

        message = "Error should have been raised about img #2 shape, other error raised instead:\n%s" % str(ex.value)
        assert "Images need to be 2-dimensional. Shape of image #2" in str(ex.value), message

    def test_error_checking_003(self):
        CoR_calc = CenterOfRotation()

        radio1 = self.data[0, :, :]
        radio2 = self.data[1, :, 0:10]

        with pytest.raises(ValueError) as ex:
            CoR_calc.find_shift(radio1, radio2)

        message = "Error should have been raised about different image shapes, " + "other error raised instead:\n%s" % str(
            ex.value
        )
        assert "Images need to be of the same shape" in str(ex.value), message


@pytest.mark.usefixtures("bootstrap_dtr")
class TestDetectorTranslation(object):
    def test_alignxc(self):
        T_calc = DetectorTranslationAlongBeam()

        shifts_v, shifts_h, found_shifts_list = T_calc.find_shift(self.align_images, self.img_pos, return_shifts=True)

        message = "Computed shifts coefficients %s and expected %s do not coincide" % (
            (shifts_v, shifts_h),
            self.expected_shifts_vh,
        )
        assert np.all(np.isclose(self.expected_shifts_vh, [shifts_v, shifts_h], atol=self.abs_tol)), message

        message = "Computed shifts %s and expected %s do not coincide" % (found_shifts_list, self.reference_shifts_list)
        assert np.all(np.isclose(found_shifts_list, self.reference_shifts_list, atol=self.abs_tol)), message

    @pytest.mark.skipif(not(__has_scipy__), reason="need scipy for this test")
    def test_alignxc_synth(self):
        T_calc = DetectorTranslationAlongBeam()

        stack = np.zeros([4, 512, 512], "d")
        for i in range(4):
            stack[i, 200 - i * 10, 200 - i * 10] = 1
        stack = scipy.ndimage.filters.gaussian_filter(stack, [0, 10, 10.0]) * 100
        x, y = np.meshgrid(np.arange(stack.shape[-1]), np.arange(stack.shape[-2]))
        for i in range(4):
            xc = x - (250 + i * 1.234)
            yc = y - (250 + i * 1.234 * 2)
            stack[i] += np.exp(-(xc * xc + yc * yc) * 0.5)
        shifts_v, shifts_h, found_shifts_list = T_calc.find_shift(
            stack, np.array([0.0, 1, 2, 3]), high_pass=1.0, return_shifts=True
        )

        message = "Found shifts per units %s and reference %s do not coincide" % ((shifts_v, shifts_h), (-1.234 * 2, -1.234))
        assert np.all(np.isclose((shifts_v, shifts_h), (-1.234 * 2, -1.234), atol=self.abs_tol)), message
