#!/usr/bin/env python3
import logging
import sys

from PyQt5.QtWidgets import QDialog, QStyledItemDelegate
from PyQt5.uic import loadUi
from PyQt5.QtCore import Qt

sys.path.append('..')
from backend.models.defaultappoptionsmodel import DefaultAppOptionsModel

class DefaultAppOptionsDelegate(QStyledItemDelegate):
    def __init__(self, model):
        super().__init__()
        self.model = model

    def paint(self, painter, option, index):
        """Paint handler:
        - Strike out disabled apps
        - Italicize custom associations
        - Bold the current default"""
        app_id, options = self.model.apps[index.row()]
        option.font.setStrikeOut(options.disabled)
        option.font.setItalic(options.custom)
        option.font.setBold(self.model.default == app_id)

        return super().paint(painter, option, index)

class SetDefaultAppDialog(QDialog):
    uifile = "ui/setdefaultappdialog.ui"
    def __init__(self, mimetypemanager, mimetype, parent=None):
        super().__init__()
        self._app = parent
        self.manager = mimetypemanager
        self.mimetype = mimetype

        # Enumerate and display a list of apps supporting this MIME type
        #self.current_app = None
        self.apps_model = DefaultAppOptionsModel(self.manager, mimetype)

        self._ui = loadUi(self.uifile, self)
        self._ui.setWindowTitle(f"Set default application for {mimetype.name()}")
        # Buttons
        self._ui.addApplication.clicked.connect(self.add_application)
        self._ui.removeApplication.clicked.connect(self.remove_application)
        self._ui.setAsDefault.clicked.connect(self.set_default)
        # ListView
        self._ui.appsView.setModel(self.apps_model)
        #self._ui.appsView.currentChanged = self.on_row_changed
        self._ui.appsView.setItemDelegate(DefaultAppOptionsDelegate(self.apps_model))
        self._ui.show()

    def add_application(self, event):
        # TODO: stub
        return

    def set_default(self, event):
        # TODO: stub
        selection = self._ui.appsView.selectedIndexes()
        if selection:
            selected_idx = selection[0]
            app_id, options = self.apps_model.apps[selected_idx.row()]
            print(f"Will set app {app_id} as default for {self.mimetype.name()}")
        return

    def remove_application(self, event):
        # TODO: stub
        return
