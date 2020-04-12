#!/usr/bin/env python3
import sys

from PyQt5.QtWidgets import QMainWindow, QApplication, QHeaderView
from PyQt5.uic import loadUi
from PyQt5.QtCore import Qt

from models.mimetypeslistmodel import MimeTypesListModel
from models.mimeapps import MimeAppsList
from models.desktopentries import DesktopEntries

class AppSelector(QMainWindow):
    """App Selector main window"""

    def __init__(self, app, uifile):
        super().__init__()
        self._app = app
        self._ui = loadUi(uifile, self)
        self._ui.show()

        # Enumerate Apps list
        self.applist = DesktopEntries()

        # Enumerate MIME Types table view
        self.mimeapps = MimeAppsList(self.applist)
        self.mimetypesmodel = MimeTypesListModel(self.mimeapps)
        self._ui.typesView.setModel(self.mimetypesmodel)
        self._ui.typesView.sortByColumn(0, Qt.AscendingOrder)

def main():
    """Entrypoint: runs program and inits UI"""
    app = QApplication(sys.argv)
    AppSelector(app, "appsel.ui")
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
