
# pylint: disable=invalid-name
from PyQt5.QtCore import Qt, QAbstractListModel, QModelIndex

class AppsListModel(QAbstractListModel):
    """
    Enumerates a list of applications (.desktop entries)
    """
    def __init__(self, desktop_entries):
        super().__init__()
        self.desktop_entries = desktop_entries
        self.refresh(first_run=True)
        self.sort(0)

    def refresh(self, first_run=False):
        self.apps = list(self.desktop_entries.entries)
        if not first_run:
            self.dataChanged.emit(QModelIndex(), QModelIndex())

    def data(self, index, role):
        app_id = self.apps[index.row()]
        if role == Qt.DisplayRole:  # Display text
            return self.desktop_entries.get_name(app_id)
        if role == Qt.DecorationRole:  # App icon
            return self.desktop_entries.get_icon(app_id)

    def sort(self, _column, order=Qt.AscendingOrder):
        """Sorts the model by the given column and order."""
        self.apps.sort(key=lambda app_id: self.desktop_entries.get_name(app_id),
                       reverse=order != Qt.AscendingOrder)

    def rowCount(self, _index):
        return len(self.desktop_entries.entries)

    def columnCount(self, _index):
        return 1
