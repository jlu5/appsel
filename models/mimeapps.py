

import configparser
import itertools
import os

from PyQt5.QtCore import Qt, QStandardPaths

class MimeAppsList():
    def __init__(self):
        print("mimeapps.list paths:", self._get_mimeapps_list_paths())

        # Read mimeapps.list from INI parser
        self.mimeapps = configparser.ConfigParser()
        self.mimeapps.read(self._get_mimeapps_list_paths())

    @staticmethod
    def _get_mimeapps_list_paths():
        """
        Returns a list of mimeapps.list paths, in order of decreasing priority.

        Based off of: https://specifications.freedesktop.org/mime-apps-spec/latest/ar01s02.html
        """
        current_desktops = os.environ.get('XDG_CURRENT_DESKTOP', '').split(':')

        user_defaults_per_desktop = list(itertools.chain.from_iterable(
            QStandardPaths.locateAll(QStandardPaths.ConfigLocation, f"mimeapps-{desktop}.list")
            for desktop in current_desktops
        ))
        user_defaults = QStandardPaths.locateAll(QStandardPaths.ConfigLocation, "mimeapps.list")

        global_defaults_per_desktop = list(itertools.chain.from_iterable(
            QStandardPaths.locateAll(QStandardPaths.ApplicationsLocation,
                                        f"mimeapps-{desktop}.list")
            for desktop in current_desktops
        ))
        global_defaults = QStandardPaths.locateAll(QStandardPaths.ApplicationsLocation, "mimeapps.list")
        return user_defaults_per_desktop + user_defaults + global_defaults_per_desktop + global_defaults

    def get_default_app(self, mimetype):
        return

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
