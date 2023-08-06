import os.path as path
from os import linesep
from configparser import ConfigParser, MissingSectionHeaderError, DuplicateOptionError
from silx.io.dictdump import dicttoh5, h5todict
from ..utils import check_supported
from ..resources.nabu_config import nabu_config, _options_levels, renamed_keys

class NabuConfigParser(object):
    def __init__(self, fname):
        """
        Nabu configuration file parser.

        Parameters
        ----------
        fname: str
            File name of the configuration file
        """
        parser = ConfigParser(
            inline_comment_prefixes=("#",) # allow in-line comments
        )
        with open(fname) as fid:
            file_content = fid.read()
        parser.read_string(file_content)
        self.parser = parser
        self.get_dict()
        self.file_content = file_content.split(linesep)

    def get_dict(self):
        # Is there an officially supported way to do this ?
        self.conf_dict = self.parser._sections

    def __str__(self):
        return self.conf_dict.__str__()

    def __repr__(self):
        return self.conf_dict.__repr__()

    def __getitem__(self, key):
        return self.conf_dict[key]


def generate_nabu_configfile(fname, config=None, sections=None, comments=True, options_level=None):
    """
    Generate a nabu configuration file.

    Parameters
    -----------
    fname: str
        Output file path.
    config: dict
        Configuration to save. If section and / or key missing will store the
        default value
    sections: list of str, optional
        Sections which should be included in the configuration file
    comments: bool, optional
        Whether to include comments in the configuration file
    options_level: str, optional
        Which "level" of options to embed in the file. Can be "required", "optional", "advanced".
        Default is "optional".
    """
    if options_level is None:
        options_level = "optional"
    check_supported(options_level, list(_options_levels.keys()), "options_level")
    options_level = _options_levels[options_level]
    parser = ConfigParser(
        inline_comment_prefixes=("#",) # allow in-line comments
    )
    if config is None:
        config = {}
    if sections is None:
        sections = nabu_config.keys()
    with open(fname, "w") as fid:
        for section, section_content in nabu_config.items():
            if section not in sections:
                continue
            if section != "dataset":
                fid.write("%s%s" % (linesep, linesep))
            fid.write("[%s]%s" % (section, linesep))
            for key, values in section_content.items():
                if options_level < _options_levels[values["type"]]:
                    continue
                if comments and values["help"].strip() != "":
                    for help_line in values["help"].split(linesep):
                        content = "# %s" % (help_line) if help_line.strip() != "" else ""
                        content = content + linesep
                        fid.write(content)
                value = values["default"]
                if section in config and key in config[section]:
                    value = config[section][key]
                fid.write("%s = %s%s" % (key, value, linesep))



def _extract_nabuconfig_section(section):
    res = {}
    for key, val in nabu_config[section].items():
        res[key] = val["default"]
    return res


def _extract_nabuconfig_keyvals():
    res = {}
    for section in nabu_config.keys():
        res[section] = _extract_nabuconfig_section(section)
    return res


def _handle_renamed_key(key, val, section):
    if val is not None:
        return key, val
    if key in renamed_keys and renamed_keys[key]["section"] == section:
        info = renamed_keys[key]
        print(
            "Option '%s' has been renamed to '%s' since version %s. It will result in an error in version %s"
            % (key, info["new_name"], info["since"], info["end_deprecation"])
        )
        val = nabu_config[section].get(info["new_name"], None)
        return info["new_name"], val
    else:
        return key, None


def validate_nabu_config(config):
    """
    Validate a nabu configuration.

    Parameters
    ----------
    config: str or dict
        Configuration. Can be a dictionary or a path to a configuration file.
    """
    if isinstance(config, str):
        config = NabuConfigParser(config).conf_dict
    res_config = {}
    for section, section_content in config.items():
        # Ignore the "other" section
        if section.lower() == "other":
            continue
        if section not in nabu_config:
            raise ValueError("Unknown section [%s]" % section)
        res_config[section] = _extract_nabuconfig_section(section)
        res_config[section].update(section_content)
        for key, value in res_config[section].items():
            opt = nabu_config[section].get(key, None)
            key, opt = _handle_renamed_key(key, opt, section)
            if opt is None:
                raise ValueError("Unknown option '%s' in section [%s]" % (key, section))
            validator = nabu_config[section][key]["validator"]
            res_config[section][key] = validator(section, key, value)
    return res_config


def export_dict_to_h5(dic, h5file, h5path, overwrite_data=True, mode="a"):
    """
    Wrapper on top of silx.io.dictdump.dicttoh5 replacing None with "None"
    """
    modified_dic = {}
    # TODO support depth > 2 ?
    for section, options in dic.items():
        modified_dic[section] = {}
        for key, value in options.items():
            val = "None" if value is None else value
            modified_dic[section][key] = val
    return dicttoh5(
        modified_dic,
        h5file=h5file,
        h5path=h5path,
        overwrite_data=overwrite_data,
        mode=mode
    )


def import_h5_to_dict(h5file, h5path):
    dic = h5todict(h5file, path=h5path, asarray=False)
    # TODO support depth > 2 ?
    for section, options in dic.items():
        modified_dic[section] = {}
        for key, value in options.items():
            val = None if value is "None" else value
            modified_dic[section][key] = val
    return modified_dic

