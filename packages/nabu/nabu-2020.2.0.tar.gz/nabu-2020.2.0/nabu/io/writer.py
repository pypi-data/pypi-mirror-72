from datetime import datetime
import numpy as np
import h5py
from silx.utils.enum import Enum
from .. import version
from .config import export_dict_to_h5


class Writer:
    """
    Base class for all writers.
    """
    def __init__(self, fname):
        self.fname = fname


class NXProcessWriter(Writer):
    def __init__(self, fname, entry=None, filemode="a"):
        """
        Initialize a NXProcessWriter.

        Parameters
        -----------
        fname: str
            Path to the HDF5 file.
        entry: str, optional
            Entry in the HDF5 file. Default is "entry"
        """
        super().__init__(fname)
        self._set_entry(entry)
        self._filemode = filemode


    def _set_entry(self, entry):
        self.entry = entry or "entry"
        data_path = "/".join([self.entry])
        if not(data_path.startswith("/")):
            data_path = "/" + data_path
        self.data_path = data_path


    def write(self, result, process_name, processing_index=0, config=None, is_frames_stack=True):
        """
        Write the result in the current NXProcess group.

        Parameters
        ----------
        result: numpy.ndarray
            Array containing the processing result
        process_name: str
            Name of the processing
        processing_index: int
            Index of the processing (in a pipeline)
        config: dict, optional
            Dictionary containing the configuration.
        """
        with h5py.File(self.fname, self._filemode, swmr=True) as fid:
            nx_entry = fid.require_group(self.data_path)
            key = "NX_class"
            if key not in nx_entry.attrs:
                nx_entry.attrs[key] = "NXentry"

            nx_process = nx_entry.require_group(process_name)
            nx_process.attrs['NX_class'] = "NXprocess"

            nx_process['program'] = "nabu"
            nx_process['version'] = version
            nx_process['date'] = datetime.now().replace(microsecond=0).isoformat()
            nx_process['sequence_index'] = np.int32(processing_index)

            if config is not None:
                export_dict_to_h5(
                    config,
                    self.fname,
                    '/'.join([nx_process.name, 'configuration']),
                    overwrite_data=True,
                    mode="a"
                )
                nx_process['configuration'].attrs['NX_class'] = "NXcollection"
            nx_data = nx_process.require_group('results')
            nx_data.attrs['NX_class'] = "NXdata"
            nx_data.attrs['signal'] = "data"
            nx_data['data'] = result
            if is_frames_stack:
                nx_data['data'].attrs['interpretation'] = "image"

            # prepare the direct access plots
            nx_process.attrs['default'] = 'results'
            key = "default"
            if key not in nx_entry.attrs:
                nx_entry.attrs[key] = '/'.join([nx_process.name, 'results'])


class NPYWriter(Writer):
    def __init__(self,  fname):
        super().__init__(fname)

    def write(self, result, *args, **kwargs):
        np.save(self.fname, result)


class NPZWriter(Writer):
    def __init__(self,  fname):
        super().__init__(fname)

    def write(self, result, *args, **kwargs):
        save_args = {"result": result}
        config = kwargs.get("config", None)
        if config is not None:
            save_args["configuration"] = config
        np.savez(self.fname, **save_args)


Writers = {
    "h5": NXProcessWriter,
    "hdf5": NXProcessWriter,
    "nx": NXProcessWriter,
    "nexus": NXProcessWriter,
    "npy": NPYWriter,
    "npz": NPZWriter,
}
