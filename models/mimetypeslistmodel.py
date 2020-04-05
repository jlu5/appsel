
# pylint: disable=invalid-name
from PyQt5.QtCore import Qt, QAbstractTableModel, QMimeDatabase, QVariant, QModelIndex
from PyQt5.QtGui import QIcon

class MimeTypesListModel(QAbstractTableModel):

    def __init__(self):
        super().__init__()

        db = QMimeDatabase()
        self.mimetypes = db.allMimeTypes()

    def data(self, index, role):
        if index.column() == 0:
            return self._get_mimetype(index, role)
        # TODO: implement fetching associated app
        return QVariant()

    def sort(self, column, order=Qt.AscendingOrder):
        if column == 0:
            self.mimetypes.sort(key=lambda mimetype: mimetype.name(),
                                reverse=order != Qt.AscendingOrder)
            self.dataChanged.emit(QModelIndex(), QModelIndex())
        # TODO: implement sorting on default app

    def _get_mimetype(self, index, role):
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

    def headerData(self, section, _orientation, role):
        if role == Qt.DisplayRole:
            if section == 0:
                return "MIME Type"
            elif section == 1:
                return "Associated application"
        return QVariant()

    def rowCount(self, _index):
        return len(self.mimetypes)

    def columnCount(self, _index):
        return 2  # hardcoded to be MIME type + app list
