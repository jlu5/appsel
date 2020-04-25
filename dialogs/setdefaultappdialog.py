#!/usr/bin/env python3
import logging
import sys

from PyQt5.QtWidgets import QDialog, QStyledItemDelegate
from PyQt5.uic import loadUi
from PyQt5.QtCore import Qt, QMimeType

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
    def __init__(self, mimetypemanager, mimetype: QMimeType, parent=None):
        super().__init__()
        self._app = parent
        self.manager = mimetypemanager
        self.mimetype = mimetype

        # Enumerate and display a list of apps supporting this MIME type
        #self.current_app = None
        self.model = DefaultAppOptionsModel(self.manager, mimetype)

        self._ui = loadUi(self.uifile, self)
        self._ui.setWindowTitle(f"Set default application for {mimetype.name()}")
        # Buttons
        self._ui.addApplication.clicked.connect(self.add_application)
        self._ui.removeApplication.clicked.connect(self.remove_application)
        self._ui.setAsDefault.clicked.connect(self.set_default)
        # ListView
        self._ui.appsView.setModel(self.model)
        #self._ui.appsView.currentChanged = self.on_row_changed
        self._ui.appsView.setItemDelegate(DefaultAppOptionsDelegate(self.model))
        self._ui.show()

    def _refresh(self):
        self.model.refresh()
        self._ui.appsView.repaint()

    def add_application(self, event):
        # TODO: stub
        return

    def set_default(self, _event):
        """Button handler: sets the default application."""
        selection = self._ui.appsView.selectedIndexes()
        if selection:
            selected_idx = selection[0]
            app_id, _options = self.model.apps[selected_idx.row()]
            self.manager.set_default_app(self.mimetype.name(), app_id)
        self._refresh()

    def remove_application(self, event):
        # TODO: stub
        return
