
import collections
import configparser
import itertools
import os
import pprint

from PyQt5.QtCore import Qt, QStandardPaths

SECTION_DEFAULTS = "Default Applications"
SECTION_ADDED = "Added Associations"
SECTION_REMOVED = "Removed Associations"

class MimeAppsList():
    def __init__(self, applist, *, paths=None):
        self.applist = applist
        if paths is None:
            paths = self._get_mimeapps_list_paths()
            print("mimeapps.list paths:", self._get_mimeapps_list_paths())

        if not paths:
            # If no paths were found, use $XDG_CONFIG_HOME/mimeapps.list (~/.config/mimeapps.list)
            paths = [os.path.join(QStandardPaths.writableLocation(QStandardPaths.ConfigLocation), "mimeapps.list")]

        # For each location of mimeapps.list, merge the definitions into a single store
        # Since each section specifies a list, we can't use configparser's built-in handling of multiple files,
        # since that overrides already seen keys
        self.mimeapps_db = collections.defaultdict(dict)
        self.mimeapps_local = None
        for path in paths:
            loader = configparser.ConfigParser()
            loader.read(path)

            # Treat the first mimeapps.list path as the writable one. Usually this will be ~/.config/mimeapps.list
            if self.mimeapps_local is None:
                self.mimeapps_local = loader

            for section in {SECTION_ADDED, SECTION_DEFAULTS, SECTION_REMOVED}:
                if loader.has_section(section):
                    db_section = self.mimeapps_db[section]
                    for key, value in loader[section].items():
                        value = value.strip(';').split(';')
                        print(f'Loaded {section} option {key}={value}')
                        existing = db_section.get(key, [])
                        db_section[key] = existing + value
        pprint.pprint(self.mimeapps_db)

    @staticmethod
    def _get_mimeapps_list_paths():
        """
        Returns a list of mimeapps.list paths, in order of decreasing priority.

        Based off of: https://specifications.freedesktop.org/mime-apps-spec/latest/ar01s02.html
        """
        current_desktops = os.environ.get('XDG_CURRENT_DESKTOP', '').split(':')

        user_defaults_per_desktop = list(itertools.chain.from_iterable(
            QStandardPaths.locateAll(QStandardPaths.ConfigLocation, f"{desktop}-mimeapps.list")
            for desktop in current_desktops
        ))
        user_defaults = QStandardPaths.locateAll(QStandardPaths.ConfigLocation, "mimeapps.list")

        global_defaults_per_desktop = list(itertools.chain.from_iterable(
            QStandardPaths.locateAll(QStandardPaths.ApplicationsLocation,
                                     f"{desktop}-mimeapps.list")
            for desktop in current_desktops
        ))
        global_defaults = QStandardPaths.locateAll(QStandardPaths.ApplicationsLocation, "mimeapps.list")
        return user_defaults_per_desktop + user_defaults + global_defaults_per_desktop + global_defaults

    def get_default_app(self, mimetype):
        #for entry in self.mimeapps_db[SECTION_DEFAULTS]:
        #    if <desktop entry exists> and <desktop entry supports type>:
        #        return entry
        return None  # Not found

    def set_default_app(self, mimetype, desktop_entry):
        return

    def is_blacklisted(self, mimetype, desktop_entry):
        return

    def set_blacklisted(self, mimetype, desktop_entry, value):
        return

    def has_association(self, mimetype, desktop_entry):
        return

    def add_association(self, mimetype, desktop_entry):
        return

    def remove_association(self, mimetype, desktop_entry):
        return
