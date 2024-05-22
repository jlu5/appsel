#!/usr/bin/env python3
import logging
import sys

from PyQt5.QtWidgets import QMainWindow, QApplication, QStyledItemDelegate
from PyQt5.uic import loadUi
from PyQt5.QtCore import Qt, QSortFilterProxyModel

from appsel.backend.models.mimetypeslistmodel import MimeTypesListModel
from appsel.backend.models.appslistmodel import AppsListModel
from appsel.backend.models.filteredappslistmodel import FilteredAppsListModel
from appsel.backend.mimetypesmanager import MimeTypesManager
from appsel.backend.desktopentries import DesktopEntriesList

from appsel.dialogs.setdefaultappdialog import SetDefaultAppDialog
from appsel.dialogs.setdefaultsbyappdialog import SetDefaultsByAppDialog

__version__ = '0.1.0'

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
        self.appslistmodel = AppsListModel(self.manager)

        # Filter models
        self.filteredmimetypesmodel = QSortFilterProxyModel(self)
        self.filteredmimetypesmodel.setFilterCaseSensitivity(False)
        self.filteredmimetypesmodel.setSourceModel(self.mimetypesmodel)
        self.filteredmimetypesmodel.setFilterKeyColumn(-1)  # search all columns
        self.filteredmimetypesmodel.sort(0, Qt.AscendingOrder)
        self.filteredappslistmodel = FilteredAppsListModel(self, self.manager, self._ui)
        self.filteredappslistmodel.setFilterCaseSensitivity(False)
        self.filteredappslistmodel.setSourceModel(self.appslistmodel)

        # UI bindings - select by MIME type tab
        self._ui.typesView.setModel(self.filteredmimetypesmodel)
        self._ui.typesView.activated.connect(self.configure_default_app)
        self._ui.typesView.sizeHintForColumn = self.types_view_size_hint
        self._ui.typesView.resizeColumnsToContents()
        self._ui.typesSearchBar.textChanged.connect(self.filteredmimetypesmodel.setFilterFixedString)

        # UI bindings - select by app tab
        self._ui.appsView.setModel(self.filteredappslistmodel)
        self._ui.appsView.activated.connect(self.configure_defaults_by_app)
        self._ui.appsView.sizeHintForColumn = self.apps_view_size_hint
        self._ui.appsView.resizeColumnsToContents()
        self._ui.appsSearchBar.textChanged.connect(self.filteredappslistmodel.setFilterFixedString)
        self._ui.showAllAppsCheckBox.stateChanged.connect(self.filteredappslistmodel.invalidate)

    def types_view_size_hint(self, column):
        if column in {1, 2}:  # File Extensions, Status
            return int(self.width() * 0.15)
        else:
            return int(self.width() * 0.32)

    def apps_view_size_hint(self, column):
        if column in {0}:  # App name
            return int(self.width() * 0.5)
        else:
            return int(self.width() * 0.15)

    def configure_default_app(self, index):
        """Launches a dialog to set the default app for a MIME type."""
        unfiltered_index = self.filteredmimetypesmodel.mapToSource(index)
        mimetype = self.mimetypesmodel.mimetypes[unfiltered_index.row()]  # type: QMimeType
        return SetDefaultAppDialog(self.manager, mimetype.name(), parent=self)

    def configure_defaults_by_app(self, index):
        """Launches a dialog to set default associations by application."""
        unfiltered_index = self.filteredappslistmodel.mapToSource(index)
        app_id = self.appslistmodel.apps[unfiltered_index.row()]  # type: QMimeType
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
