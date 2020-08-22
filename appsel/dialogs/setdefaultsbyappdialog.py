#!/usr/bin/env python3
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog
from PyQt5.uic import loadUi

from appsel.backend.models.defaultsforappmodel import DefaultsForAppModel
from appsel.itemdelegates import DefaultAppOptionsDelegate

class SetDefaultsByAppDialog(QDialog):
    """
    Dialog to add a custom application for a MIME type.
    """
    BLACKLISTED_CATEGORIES = ["inode/"]
    uifile = "ui/setdefaultsbyappdialog.ui"
    def __init__(self, manager, app_id, parent=None):
        super().__init__()
        self._app = parent
        self.manager = manager

        self.app_id = app_id
        self.model = DefaultsForAppModel(manager, app_id)
        self.delegate = DefaultAppOptionsDelegate(self.model, "supported_types")

        self._ui = loadUi(self.uifile, self)
        # XXX: internationalize
        self._ui.setWindowTitle(f"Set defaults for app {app_id}")
        # Buttons
        self._ui.selectAllButton.clicked.connect(self.select_all)
        self._ui.deselectAllButton.clicked.connect(self.deselect_all)
        # ListView
        self._ui.tableView.setModel(self.model)
        self._ui.tableView.setItemDelegate(self.delegate)
        self._ui.tableView.resizeColumnsToContents()
        self._ui.show()

    def _check_all(self, state):
        """
        Checks or unchecks all items in the underlying model.
        """
        for row in range(self.model.rowCount()):
            index = self.model.index(row, 0)
            self.model.setData(index, state, Qt.CheckStateRole)

    def select_all(self):
        """
        Handler for the select all button.
        """
        self._check_all(Qt.Checked)

    def deselect_all(self):
        """
        Handler for the deselect all button.
        """
        self._check_all(Qt.Unchecked)
