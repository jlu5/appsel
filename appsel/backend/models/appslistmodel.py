
# pylint: disable=invalid-name
from PyQt5.QtCore import Qt, QAbstractListModel, QModelIndex, QVariant

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
        self.apps = list(filter(self.desktop_entries.is_shown, self.desktop_entries.entries))
        if not first_run:
            self.dataChanged.emit(QModelIndex(), QModelIndex())

    def data(self, index, role):
        app_id = self.apps[index.row()]
        if role == Qt.DisplayRole:  # Display text
            return self.desktop_entries.get_name(app_id)
        if role == Qt.DecorationRole:  # App icon
            return self.desktop_entries.get_icon(app_id)
        return QVariant()

    def sort(self, _column, order=Qt.AscendingOrder):
        """Sorts the model by the given column and order."""
        self.apps.sort(key=lambda app_id: self.desktop_entries.get_name(app_id).casefold(),
                       reverse=order != Qt.AscendingOrder)

    def rowCount(self, _index):
        """
        Return list of rows in the model.
        """
        return len(self.apps)

    def columnCount(self, _index):
        """
        Return list of columns in the model.
        """
        return 1
