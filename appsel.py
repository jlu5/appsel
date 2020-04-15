#!/usr/bin/env python3
import logging
import sys

from PyQt5.QtWidgets import QMainWindow, QApplication, QHeaderView
from PyQt5.uic import loadUi
from PyQt5.QtCore import Qt

from backend.models.mimetypeslistmodel import MimeTypesListModel
from backend.mimetypesmanager import MimeTypesManager
from backend.desktopentries import DesktopEntriesList

from dialogs.setdefaultappdialog import SetDefaultAppDialog

class AppSelector(QMainWindow):
    """App Selector main window"""

    def __init__(self, app, uifile):
        super().__init__()
        self._app = app
        self._ui = loadUi(uifile, self)
        self._ui.show()

        # Enumerate Apps list
        self.applist = DesktopEntriesList()

        # Enumerate MIME Types table view
        self.manager = MimeTypesManager(self.applist)
        self.mimetypesmodel = MimeTypesListModel(self.manager)
        self._ui.typesView.setModel(self.mimetypesmodel)
        self._ui.typesView.sortByColumn(0, Qt.AscendingOrder)
        self._ui.typesView.activated.connect(self.mime_type_settings)
        self._ui.typesView.sizeHintForColumn = self.types_view_size_hint_for_column
        self._ui.typesView.resizeColumnsToContents()

    def types_view_size_hint_for_column(self, column):
        if column in {1, 2}:  # File Extensions, Status
            return int(self.width() * 0.15)
        else:
            return int(self.width() * 0.32)

    def mime_type_settings(self, index):
        """Launches a dialog to set the default app for a MIME type."""
        mimetype = self.mimetypesmodel.mimetypes[index.row()]  # type: QMimeType
        SetDefaultAppDialog(self.manager, mimetype)

def main():
    """Entrypoint: runs program and inits UI"""
    logging.basicConfig(level=logging.DEBUG)
    app = QApplication(sys.argv)
    AppSelector(app, "ui/appsel.ui")
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
