
# pylint: disable=invalid-name
import functools

from PyQt5.QtCore import Qt, QAbstractListModel, QVariant, QModelIndex
from PyQt5.QtGui import QIcon

class SimpleAppListModel(QAbstractListModel):
    """
    A model to represent a read only list of applications.
    This is used in the default app selector when setting defaults by MIME type.
    """
    def __init__(self, desktop_entries, apps):
        super().__init__()

        self.desktop_entries = desktop_entries
        self.apps = apps

    def data(self, index, role):
        app_id = self.apps[index.row()]
        if role == Qt.DisplayRole:  # Display text
            return self.desktop_entries.get_name(app_id)
        if role == Qt.DecorationRole:  # App icon
            return self.desktop_entries.get_icon(app_id)

    def sort(self, _column, order=Qt.AscendingOrder):
        """Sorts the model by the given column and order."""
        self.apps.sort(reverse=order != Qt.AscendingOrder)
        self.dataChanged.emit(QModelIndex(), QModelIndex())

    def rowCount(self, _index):
        return len(self.apps)
