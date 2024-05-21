
# pylint: disable=invalid-name
from PyQt5.QtCore import Qt, QAbstractTableModel, QVariant, QModelIndex
from PyQt5.QtGui import QFont

from appsel.backend import utils

class MimeTypesListModel(QAbstractTableModel):

    COLUMNS = ["MIME Type", "File Extensions", "Status", "Default Application"]

    def __init__(self, mimetypemanager):
        super().__init__()

        self.manager = mimetypemanager
        self.db = mimetypemanager.qmimedb
        self.mimetypes = []
        self.load_mime_types()
        self._default_app_cache = {}

    def load_mime_types(self):
        self.mimetypes.clear()
        # Only show MIME types that have at least one app
        for qmimetype in self.db.allMimeTypes():
            if qmimetype.name() in self.manager.mimeinfo_cache:
                self.mimetypes.append(qmimetype)

    def _get_mimetype(self, index, role):
        """Returns display data for the MIME type column."""
        mimetype = self.mimetypes[index.row()]

        if role == Qt.DisplayRole:
            return mimetype.name()
        if role == Qt.DecorationRole:
            return utils.get_mimetype_icon(mimetype)
        if role == Qt.FontRole:
            font = QFont()
            font.setBold(self.manager.has_default(mimetype.name()))
            return font

        return QVariant()

    def _get_extensions(self, index, role):
        """Returns display data for the File Extensions column."""
        mimetype = self.mimetypes[index.row()]

        if role == Qt.DisplayRole:
            return ",".join(mimetype.suffixes())
        if role == Qt.FontRole:
            font = QFont()
            font.setBold(self.manager.has_default(mimetype.name()))
            return font

        return QVariant()

    def _get_status(self, index, role):
        """Returns display data for the Status column."""
        mimetype = self.mimetypes[index.row()]
        default_is_set = self.manager.has_default(mimetype.name())

        if role == Qt.DisplayRole:
            return "User defined" if default_is_set else "Automatic"
        if role == Qt.FontRole:
            font = QFont()
            font.setBold(default_is_set)
            return font

        return QVariant()

    def _get_default_app(self, index, role):
        """Returns display data for the default application column."""
        mimetype = self.mimetypes[index.row()]
        if role == Qt.FontRole:
            font = QFont()
            font.setBold(self.manager.has_default(mimetype.name()))
            return font

        if mimetype.name() in self._default_app_cache:
            default_app_id = self._default_app_cache[mimetype.name()]
        else:
            self._default_app_cache[mimetype.name()] = default_app_id = self.manager.get_default_app(mimetype.name())

        if default_app_id:
            if role == Qt.DisplayRole:  # Display text
                return self.manager.desktop_entries.get_name(default_app_id)
            if role == Qt.DecorationRole:  # App icon
                return self.manager.desktop_entries.get_icon(default_app_id)
        else:  # No default app found
            if role == Qt.DisplayRole:
                return 'None selected'

        return QVariant()

    def data(self, index, role):
        accessors = [self._get_mimetype, self._get_extensions, self._get_status, self._get_default_app]
        try:
            return accessors[index.column()](index, role)
        except IndexError:
            return QVariant()

    def refresh(self):
        """Refresh the data in this model."""
        self._default_app_cache.clear()
        self.dataChanged.emit(QModelIndex(), QModelIndex())

    def sort(self, column, order=Qt.AscendingOrder):
        """Sorts the model by the given column and order."""
        # Note column = -1 is also allowed, meaning the natural order of the list
        # https://doc.qt.io/qt-5/qtableview.html#sortByColumn
        if column <= 0:
            self.mimetypes.sort(key=lambda mimetype: mimetype.name(),
                                reverse=order != Qt.AscendingOrder)
        elif column == 1:
            self.mimetypes.sort(key=lambda qmimetype: qmimetype.preferredSuffix() or '\uFFFF',
                                reverse=order != Qt.AscendingOrder)
        elif column == 2:
            self.mimetypes.sort(key=lambda qmimetype: self.manager.has_default(qmimetype.name()),
                                reverse=order != Qt.AscendingOrder)
        elif column == 3:
            def _sort_by_app(mimetype):
                # \uFFFF is a quick hack to make types without a default show up last
                return self.manager.get_default_app(mimetype.name()) or '\uFFFF'

            self.mimetypes.sort(key=_sort_by_app,
                                reverse=order != Qt.AscendingOrder)
        self.refresh()

    def headerData(self, section, orientation, role):
        if role == Qt.DisplayRole and orientation == Qt.Horizontal:
            return self.COLUMNS[section]
        return QVariant()

    def rowCount(self, _index):
        """
        Return list of rows in the model.
        """
        return len(self.mimetypes)

    def columnCount(self, _index):
        """
        Return list of columns in the model.
        """
        return len(self.COLUMNS)
