#!/usr/bin/env python3

from PyQt5.QtWidgets import QDialog
from PyQt5.uic import loadUi

from appsel.backend.models.appslistmodel import AppsListModel

class AddCustomAppDialog(QDialog):
    """
    Dialog to add a custom application for a MIME type.
    """
    uifile = "ui/addcustomappdialog.ui"
    def __init__(self, desktop_entries, parent=None):
        super().__init__()
        self._app = parent
        self.desktop_entries = desktop_entries

        self.model = AppsListModel(desktop_entries)

        # Selection state
        self.current_index = None

        self._ui = loadUi(self.uifile, self)
        # XXX: internationalize
        self._ui.setWindowTitle("Add a custom application")
        # Buttons
        self._ui.buttonBox.accepted.connect(self.accept)
        self._ui.buttonBox.rejected.connect(self.reject)
        # ListView
        self._ui.appsView.setModel(self.model)
        self._ui.appsView.selectionModel().selectionChanged.connect(self.on_row_changed)
        self._ui.show()

    def on_row_changed(self, selected, _deselected):
        if selected.indexes():
            self.current_index = selected.indexes()[0].row()

    def get_selected_app(self):
        if self.current_index is not None:
            try:
                return self.model.apps[self.current_index]
            except IndexError:
                return None
