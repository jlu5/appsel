
# pylint: disable=invalid-name
import functools

from PyQt5.QtCore import Qt, QAbstractListModel, QVariant, QModelIndex, QMimeType
from PyQt5.QtGui import QIcon

class DefaultAppOptionsModel(QAbstractListModel):
    """
    A model to represent app choices in the when setting the defaults for a MIME type.
    """
    def __init__(self, manager, mimetype: QMimeType):
        super().__init__()

        self.manager = manager
        self.mimetype = mimetype
        self.default = None
        self.refresh()
        self.apps = list(self.manager.get_supported_apps(mimetype.name()).items())

    def refresh(self):
        self.default = self.manager.get_default_app(self.mimetype.name())

    def data(self, index, role):
        app_id, options = self.apps[index.row()]
        if role == Qt.DisplayRole:  # Display text
            prefix = ''
            if options.disabled:
                prefix += "(disabled) "
            if options.custom:
                prefix += "(custom) "
            return prefix + self.manager.desktop_entries.get_name(app_id)
        if role == Qt.DecorationRole:  # App icon
            return self.manager.desktop_entries.get_icon(app_id)

    def sort(self, _column, order=Qt.AscendingOrder):
        """Sorts the model by the given column and order."""
        self.apps.sort(key=lambda item: item[0], reverse=order != Qt.AscendingOrder)
        self.dataChanged.emit(QModelIndex(), QModelIndex())

    def rowCount(self, _index):
        return len(self.apps)
