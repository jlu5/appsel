#!/usr/bin/env python3
import logging
import sys

from PyQt5.QtWidgets import QDialog
from PyQt5.uic import loadUi
from PyQt5.QtCore import Qt

sys.path.append('..')
from backend.models.simpleapplistmodel import SimpleAppListModel

class SetDefaultAppDialog(QDialog):
    uifile = "ui/setdefaultappdialog.ui"
    def __init__(self, mimetypemanager, mimetype, parent=None):
        super().__init__()
        self._app = parent
        self.manager = mimetypemanager
        self.mimetype = mimetype

        # Enumerate and display a list of apps supporting this MIME type
        self.current_app = None
        self.apps = self.manager.get_supported_apps(mimetype.name())
        self.apps_model = SimpleAppListModel(self.manager.desktop_entries, self.apps)

        self._ui = loadUi(self.uifile, self)
        self._ui.setWindowTitle(f"Set default application for {mimetype.name()}")
        # Buttons
        self._ui.addApplication.clicked.connect(self.add_application)
        self._ui.removeApplication.clicked.connect(self.remove_application)
        self._ui.setAsDefault.clicked.connect(self.set_default)
        # ListView
        self._ui.appsView.setModel(self.apps_model)
        self._ui.appsView.currentChanged = self.on_row_changed
        self._ui.show()

    def on_row_changed(self, current, _previous):
        self.current_app = self.apps[current.row()]

    def add_application(self, event):
        return  # TODO: stub

    def set_default(self, event):
        if self.current_app:
            print(f"Will set app {self.current_app} as default for {self.mimetype.name()}")
        return

    def remove_application(self, event):
        return
