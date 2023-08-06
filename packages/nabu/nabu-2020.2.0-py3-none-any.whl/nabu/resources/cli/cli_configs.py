#
# Default configuration for CLI tools
#

# Default configuration for "bootstrap" command

BootstrapConfig = {
    "bootstrap": {
        "help": "Bootstrap a configuration file from scratch.",
        "action": "store_const",
        "const": 1,
    },
    "convert": {
        "help": "Convert a PyHST configuration file to a nabu configuration file.",
        "default": "",
    },
    "output": {
        "help": "Output filename",
        "default": "nabu.conf",
    },
    "nocomments": {
        "help": "Remove the comments in the configuration file (default: False)",
        "action": "store_const",
        "const": 1,
    },
    "level": {
        "help": "Level of options to embed in the configuration file. Can be 'required', 'optional', 'advanced'.",
        "default": "optional",
    },
}


# Default configuration for "validate" command

ValidateConfig = {
    "input_file": {
        "help": "Nabu input file",
        "mandatory": True,
    },
}


# Default configuration for "reconstruct" command

ReconstructConfig = {
    "input_file": {
        "help": "Nabu input file",
        "default": "",
        "mandatory": True,
    },
    "log_file": {
        "help": "Log file. Default is nabu.log",
        "default": "nabu.log",
    },
    "slice": {
        "help": "Slice(s) indice(s) to reconstruct, in the format z1-z2. Default is the whole volume.",
        "default": "",
    },
    "compute": {
        "help": "Computation distribution method. Can be 'local' or 'slurm'",
        "default": "local",
    },
    "nodes": {
        "help": "Number of computing nodes to use. Ignored if --compute is set to 'local'.",
        "default": 1,
        "type": int,
    },
    "energy": {
        "help": "Beam energy in keV. DEPRECATED, was used to patch missing fields in BCU HDF5 file.",
        "default": -1,
        "type": float,
    },
}
