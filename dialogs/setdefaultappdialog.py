#!/usr/bin/env python3
import logging
import sys

from PyQt5.QtWidgets import QDialog, QStyledItemDelegate
from PyQt5.uic import loadUi
from PyQt5.QtCore import Qt, QMimeType, QModelIndex

sys.path.append('..')
from backend.models.defaultappoptionsmodel import DefaultAppOptionsModel

class DefaultAppOptionsDelegate(QStyledItemDelegate):
    def __init__(self, model: DefaultAppOptionsModel, mimetype: QMimeType):
        super().__init__()
        self.model = model
        self.mimetype = mimetype

    def paint(self, painter, option, index):
        """Paint handler:
        - Strike out disabled apps
        - Italicize custom associations
        - Bold the current default app
        """
        app_id, options = self.model.apps[index.row()]
        option.font.setStrikeOut(options.disabled)
        option.font.setItalic(options.custom)

        # XXX: ugly attribute chaining
        default = self.model.manager.get_default_app(self.mimetype.name())
        option.font.setBold(default == app_id)

        return super().paint(painter, option, index)

class SetDefaultAppDialog(QDialog):
    uifile = "ui/setdefaultappdialog.ui"
    def __init__(self, mimetypemanager, mimetype: QMimeType, parent=None):
        super().__init__()
        self._app = parent
        self.manager = mimetypemanager
        self.mimetype = mimetype

        self.model = DefaultAppOptionsModel(self.manager, mimetype)
        self.delegate = DefaultAppOptionsDelegate(self.model, mimetype)
        self.current_index = None

        self._ui = loadUi(self.uifile, self)
        self._ui.setWindowTitle(f"Set default application for {mimetype.name()}")
        # Buttons
        self._ui.addApplication.clicked.connect(self.on_add_application)
        self._ui.removeApplication.clicked.connect(self.on_remove_disable_application)
        self._ui.setAsDefault.clicked.connect(self.on_set_default)
        # ListView
        self._ui.appsView.setModel(self.model)
        self._ui.appsView.selectionModel().selectionChanged.connect(self.on_row_changed)
        self._ui.appsView.setItemDelegate(self.delegate)
        self._ui.show()

    def on_row_changed(self, selected, _deselected):
        if selected.indexes():
            self.current_index = selected.indexes()[0].row()

    def on_add_application(self, event):
        # TODO: stub
        return

    def on_set_default(self, _event):
        """Button handler: set or clear the default application."""
        if self.current_index is not None:
            app_id, _options = self.model.apps[self.current_index]

            # Clear the default app if it matches the system default
            if app_id == self.manager.get_default_app(self.mimetype.name()):
                self.manager.clear_default_app(self.mimetype.name())
            else:
                self.manager.set_default_app(self.mimetype.name(), app_id)

            self.model.refresh()
            if self._app:
                self._app.refresh()

    def on_remove_disable_application(self, event):
        # TODO: stub
        return
