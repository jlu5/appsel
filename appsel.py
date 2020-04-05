#!/usr/bin/env python3
import configparser
import itertools
import os

import xdg.BaseDirectory

SECTION_DEFAULTS = "Default Applications"
SECTION_ADDED    = "Added Associations"
SECTION_REMOVED  = "Removed Associations"

def get_mimeapps_list_paths():
    """
    Returns a list of mimeapps.list paths, in order of decreasing priority.

    Based off of: https://specifications.freedesktop.org/mime-apps-spec/latest/ar01s02.html
    """
    current_desktops = os.environ.get('XDG_CURRENT_DESKTOP', '').split(':')
    user_defaults_per_desktop = list(itertools.chain.from_iterable(
        xdg.BaseDirectory.load_config_paths(f"mimeapps-{desktop}.list") for desktop in current_desktops
    ))
    user_defaults = list(xdg.BaseDirectory.load_config_paths("mimeapps.list"))
    global_defaults_per_desktop = list(itertools.chain.from_iterable(
        xdg.BaseDirectory.load_config_paths(f"mimeapps-{desktop}.list") for desktop in current_desktops
    ))
    global_defaults = list(xdg.BaseDirectory.load_data_paths("applications/mimeapps.list"))
    return user_defaults_per_desktop + user_defaults + global_defaults_per_desktop + global_defaults

def read_file_types():
    mimeapps = configparser.ConfigParser()
    mimeapps.read(get_mimeapps_list_paths())
    return mimeapps

data = read_file_types()
for section in data.sections():
    print(section, data.options(section))
