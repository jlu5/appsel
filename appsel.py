#!/usr/bin/env python3
import configparser
import itertools
import os
import sys

from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5.uic import loadUi
from PyQt5.QtCore import QStandardPaths

SECTION_DEFAULTS = "Default Applications"
SECTION_ADDED    = "Added Associations"
SECTION_REMOVED  = "Removed Associations"

class AppSelector(QMainWindow):
    """App Selector main window"""

    def __init__(self, app, uifile):
        super().__init__()
        self._app = app
        self._ui = loadUi(uifile, self)
        self._ui.show()
        print("mimeapps.list paths:", self._get_mimeapps_list_paths())

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

def main():
    """Entrypoint: runs program and inits UI"""
    app = QApplication(sys.argv)
    AppSelector(app, "appsel.ui")
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
