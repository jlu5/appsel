#!/usr/bin/env python3
import logging
import sys

from PyQt5.QtWidgets import QMainWindow, QApplication, QStyledItemDelegate
from PyQt5.uic import loadUi
from PyQt5.QtCore import Qt

from appsel.backend.models.mimetypeslistmodel import MimeTypesListModel
from appsel.backend.models.appslistmodel import AppsListModel
from appsel.backend.mimetypesmanager import MimeTypesManager
from appsel.backend.desktopentries import DesktopEntriesList

from appsel.dialogs.setdefaultappdialog import SetDefaultAppDialog
from appsel.dialogs.setdefaultsbyappdialog import SetDefaultsByAppDialog

__version__ = '0.1.0'

class MimeTypesListDelegate(QStyledItemDelegate):
    def __init__(self, model):
        super().__init__()
        self.model = model
        self.manager = model.manager

    def paint(self, painter, option, index):
        """Paint handler: bold every row where the default application has been set."""
        mimetype = self.model.mimetypes[index.row()]
        if self.manager.has_default(mimetype.name()):
            option.font.setBold(True)

        return super().paint(painter, option, index)

class AppSelector(QMainWindow):
    """App Selector main window"""

    def __init__(self, app, uifile):
        super().__init__()
        self._app = app
        self._ui = loadUi(uifile, self)
        self._ui.show()

        # Initialize backend
        self.desktop_entries = DesktopEntriesList()
        self.manager = MimeTypesManager(self.desktop_entries)
        self.mimetypesmodel = MimeTypesListModel(self.manager)
        self.appslistmodel = AppsListModel(self.desktop_entries)

        # UI bindings
        self._ui.typesView.setModel(self.mimetypesmodel)
        self._ui.typesView.sortByColumn(0, Qt.AscendingOrder)
        self._ui.typesView.activated.connect(self.configure_default_app)
        self._ui.typesView.sizeHintForColumn = self.types_view_size_hint_for_column
        self._ui.typesView.resizeColumnsToContents()
        self._ui.typesView.setItemDelegate(MimeTypesListDelegate(self.mimetypesmodel))
        self._ui.appsView.setModel(self.appslistmodel)
        self._ui.appsView.activated.connect(self.configure_defaults_by_app)

    def types_view_size_hint_for_column(self, column):
        if column in {1, 2}:  # File Extensions, Status
            return int(self.width() * 0.15)
        else:
            return int(self.width() * 0.32)

    def configure_default_app(self, index):
        """Launches a dialog to set the default app for a MIME type."""
        mimetype = self.mimetypesmodel.mimetypes[index.row()]  # type: QMimeType
        return SetDefaultAppDialog(self.manager, mimetype.name(), parent=self)

    def configure_defaults_by_app(self, index):
        """Launches a dialog to set default associations by application."""
        app_id = self.appslistmodel.apps[index.row()]  # type: QMimeType
        return SetDefaultsByAppDialog(self.manager, app_id, parent=self)

    def refresh(self):
        """Refresh root-level model instances."""
        logging.debug("Called root refresh() method")
        self.mimetypesmodel.refresh()

def main():
    """Entrypoint: runs program and inits UI"""
    logging.basicConfig(level=logging.DEBUG)
    app = QApplication(sys.argv)
    app.setApplicationName('appsel')
    app.setApplicationVersion(__version__)
    AppSelector(app, "ui/appsel.ui")
    sys.exit(app.exec_())
