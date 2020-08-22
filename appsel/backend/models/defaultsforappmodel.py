
# pylint: disable=invalid-name
from PyQt5.QtCore import Qt, QAbstractListModel, QMimeDatabase, QModelIndex, QVariant

from appsel.backend import utils

class DefaultsForAppModel(QAbstractListModel):
    """
    Represents a list of MIME types that an application supports.
    """
    def __init__(self, manager, app_id: str):
        super().__init__()

        self.manager = manager
        self.app_id = app_id
        self.refresh(first_run=True)

    def refresh(self, first_run=False):
        self.supported_types = list(self.manager.get_supported_types(self.app_id).items())
        if not first_run:
            self.dataChanged.emit(QModelIndex(), QModelIndex())

    def data(self, index, role):
        """
        Return a list of MIME types that the app supports."""
        mimetype, options = self.supported_types[index.row()]
        if role == Qt.DisplayRole:  # Display text
            prefix = ''
            if options.disabled:
                prefix += "(disabled) "
            if options.custom:
                prefix += "(custom) "
            return prefix + mimetype
        if role == Qt.DecorationRole:
            qm = self.manager.qmimedb.mimeTypeForName(mimetype)
            return utils.get_mimetype_icon(qm)
        if role == Qt.CheckStateRole:
            return self.manager.get_default_app(mimetype) == self.app_id
        return QVariant()

    def flags(self, index):
        """
        Return Qt item flags for the given index.
        """
        default_flags = super().flags(index)
        if index.isValid():
            return default_flags | Qt.ItemIsUserCheckable
        return default_flags

    def sort(self, _column, order=Qt.AscendingOrder):
        """Sorts the model by the given column and order."""
        self.apps.sort(key=lambda item: item[0], reverse=order != Qt.AscendingOrder)

    def rowCount(self, _index):
        """
        Return list of rows in the model.
        """
        return len(self.supported_types)