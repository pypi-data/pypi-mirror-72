#!/usr/bin/env python

import os
from .utils import parse_params_values
from .cli_configs import ReconstructConfig
from ...resources.processconfig import ProcessConfig
from ...app.fullfield import FullFieldPipeline
from ...cuda.utils import __has_pycuda__
if __has_pycuda__:
    from ...app.fullfield_cuda import CudaFullFieldPipeline, CudaFullFieldPipelineLimitedMemory
from ..logger import Logger
from ... import version


def get_subregion(slices_indices, radio_nz):
    if len(slices_indices) == 0:
        return (0, radio_nz)
    try:
        if "-" in slices_indices:
            z_start, z_stop = slices_indices.split("-")
            z_start = int(z_start)
            z_stop = int(z_stop)
        else:
            z_idx = int(slices_indices)
            z_start = z_idx
            z_stop = z_idx + 1
    except Exception as exc:
        print("Could not interpret slice indices: %s")
        print(exc)
        exit(1)
    return (z_start, z_stop)



def check_margin(subregion, n_z, logger, min_delta_z=10):
    delta_z = subregion[-1] - subregion[-2]
    if delta_z >= min_delta_z:
        return subregion
    if n_z < min_delta_z:
        logger.error("Need at least %d detector rows to perform phase/unsharp properly. Results will probably be inaccurate." % min_delta_z)
        return (0, n_z)
    logger.warning("Processing at least 10 detector rows for phase/unsharp")
    hz1 = min_delta_z // 2
    hz2 = min_delta_z - hz1
    zmin, zmax = subregion
    zmin = max(zmin - hz1, 0)
    zmax = min(zmax + hz2, n_z)
    if zmax - zmin < min_delta_z:
        zmin = max(zmin - hz1, 0)
        zmax = min(zmax + hz2, n_z)
    return (zmin, zmax)


def get_reconstruction_region(arg_slice, process_config, logger):
    n_z = process_config.dataset_infos._radio_dims_notbinned[-1]
    rec_opts = process_config.nabu_config["reconstruction"]

    if arg_slice == "":
        # This will be handled in future versions by inspecting available memory
        logger.warning("The argument --slice was not provided. This might result in insufficient memory errors.")
        subregion = (rec_opts["start_z"], rec_opts["end_z"])
        #
    else:
        subregion = get_subregion(
            arg_slice,
            process_config.dataset_infos.radio_dims[-1]
        )
    delta_z = subregion[-1] - subregion[-2]
    # This will be handled in future versions by inspecting available memory
    if delta_z == n_z:
        logger.warning("It seems that all the volume will be reconstructed. This will probably result in insufficient memory errors. To avoid this, please provide --slice argument or start_z and end_z in parameters file")
    steps = process_config.processing_steps
    if "phase" in steps or "unsharp_mask" in steps:
        subregion = check_margin(subregion, n_z, logger)
    #
    return subregion


def main():
    args = parse_params_values(
        ReconstructConfig,
        parser_description="Perform a tomographic reconstruction.",
        program_version="nabu " + version
    )
    proc = ProcessConfig(args["input_file"])

    logger = Logger(
        "nabu",
        level=proc.nabu_config["about"]["verbosity"],
        logfile=args["log_file"]
    )

    subregion = get_reconstruction_region(args["slice"].strip(), proc, logger)
    logger.info("Going to reconstruct slices %s" % str(subregion))
    subregion = (None, None) + subregion

    # (hopefully) temporary patch
    if "phase" in proc.processing_steps:
        if args["energy"] > 0:
            logger.warning("Using user-provided energy %.2f keV" % args["energy"])
            proc.dataset_infos.dataset_scanner._energy = args["energy"]
            proc.processing_options["phase"]["energy_kev"] = args["energy"]
        if proc.dataset_infos.energy  < 1e-3 and proc.nabu_config["phase"]["method"] != None:
            msg = "No information on energy. Cannot retrieve phase. Please use the --energy option"
            logger.fatal(msg)
            raise ValueError(msg)
    #

    if __has_pycuda__:
        PipelineCls = CudaFullFieldPipeline
    else:
        PipelineCls = FullFieldPipeline

    P = PipelineCls(
        proc,
        subregion,
        logger=logger,
    )
    P.process_chunk()




if __name__ == "__main__":
    main()
