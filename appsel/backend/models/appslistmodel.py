
# pylint: disable=invalid-name
from PyQt5.QtCore import Qt, QAbstractTableModel, QModelIndex, QVariant

class AppsListModel(QAbstractTableModel):
    """
    Enumerates a list of applications (.desktop entries)
    """
    COLUMNS = ["Application", "# Supported File Types", "# Defaults"]
    def __init__(self, manager):
        super().__init__()
        self.manager = manager
        self.desktop_entries = manager.desktop_entries
        self.refresh(first_run=True)
        self.sort(0)

    def refresh(self, first_run=False):
        self.apps = list(filter(self.desktop_entries.is_shown, self.desktop_entries.entries))
        if not first_run:
            self.dataChanged.emit(QModelIndex(), QModelIndex())

    def _get_app_name(self, index, role):
        app_id = self.apps[index.row()]
        if role == Qt.DisplayRole:  # Display text
            return self.desktop_entries.get_name(app_id)
        if role == Qt.DecorationRole:  # App icon
            return self.desktop_entries.get_icon(app_id)
        return QVariant()

    def _get_num_supported_types(self, index, role):
        app_id = self.apps[index.row()]
        if role == Qt.DisplayRole:  # Display text
            return len(self.manager.get_supported_types(app_id))
        return QVariant()

    def _get_num_defaults(self, index, role):
        app_id = self.apps[index.row()]
        if role == Qt.DisplayRole:  # Display text
            supported_types = self.manager.get_supported_types(app_id)
            return len([options for options in supported_types.values()
                        if options.default])
        return QVariant()

    def data(self, index, role):
        accessors = [self._get_app_name, self._get_num_supported_types, self._get_num_defaults]
        try:
            return accessors[index.column()](index, role)
        except IndexError:
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

    def headerData(self, section, orientation, role):
        if role == Qt.DisplayRole and orientation == Qt.Horizontal:
            return self.COLUMNS[section]
        return QVariant()

    def columnCount(self, _index):
        """
        Return list of columns in the model.
        """
        return len(self.COLUMNS)
