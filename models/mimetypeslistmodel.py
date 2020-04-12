
# pylint: disable=invalid-name
import functools

from PyQt5.QtCore import Qt, QAbstractTableModel, QMimeDatabase, QVariant, QModelIndex
from PyQt5.QtGui import QIcon

class MimeTypesListModel(QAbstractTableModel):

    def __init__(self, mimetypemanager):
        super().__init__()

        db = QMimeDatabase()
        self.mimetypemanager = mimetypemanager
        self.mimetypes = db.allMimeTypes()

    def _get_mimetype(self, index, role):
        """Returns display data for the MIME type column."""
        mimetype = self.mimetypes[index.row()]

        if role == Qt.DisplayRole:
            return mimetype.name()
        if role == Qt.DecorationRole:
            # Show the icon for the MIME type, falling back to the generic type icon
            # or the "unknown type" icon if it's missing in the current icon theme
            fallback_unknown = QIcon.fromTheme("unknown")
            fallback_generic = QIcon.fromTheme(mimetype.genericIconName(), fallback_unknown)
            return QIcon.fromTheme(mimetype.iconName(), fallback_generic)

        return QVariant()

    def _get_default_app(self, index, role):
        """Returns display data for the default application column."""
        mimetype = self.mimetypes[index.row()]
        default_app_id = self.mimetypemanager.get_default_app(mimetype.name())

        if default_app_id:
            if role == Qt.DisplayRole:  # Display text
                return self.mimetypemanager.desktop_entries.get_name(default_app_id)
            if role == Qt.DecorationRole:  # App icon
                return self.mimetypemanager.desktop_entries.get_icon(default_app_id)
        else:  # No default app found
            if role == Qt.DisplayRole:
                return 'None selected'

        return QVariant()

    @functools.lru_cache(maxsize=None)
    def data(self, index, role):
        if index.column() == 0:
            return self._get_mimetype(index, role)
        if index.column() == 1:
            return self._get_default_app(index, role)
        return QVariant()

    def _refresh_data(self):
        self.data.cache_clear()
        self.dataChanged.emit(QModelIndex(), QModelIndex())

    def sort(self, column, order=Qt.AscendingOrder):
        """Sorts the model by the given column and order."""
        # Note column = -1 is also allowed, meaning the natural order of the list
        # https://doc.qt.io/qt-5/qtableview.html#sortByColumn
        if column <= 0:
            self.mimetypes.sort(key=lambda mimetype: mimetype.name(),
                                reverse=order != Qt.AscendingOrder)
        if column == 1:
            def _sort_by_app(mimetype):
                # \uFFFF is a quick hack to make types without a default show up last
                return self.mimetypemanager.get_default_app(mimetype.name()) or '\uFFFF'

            self.mimetypes.sort(key=_sort_by_app,
                                reverse=order != Qt.AscendingOrder)
        self._refresh_data()

    def headerData(self, section, _orientation, role):
        if role == Qt.DisplayRole:
            if section == 0:
                return "MIME Type"
            elif section == 1:
                return "Default Application"
        return QVariant()

    def rowCount(self, _index):
        return len(self.mimetypes)

    def columnCount(self, _index):
        return 2  # hardcoded to be MIME type + app list
