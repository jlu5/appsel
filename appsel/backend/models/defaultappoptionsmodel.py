
# pylint: disable=invalid-name
from PyQt5.QtCore import Qt, QAbstractListModel, QModelIndex, QMimeType

class DefaultAppOptionsModel(QAbstractListModel):
    """
    A model to represent app choices in the when setting the defaults for a MIME type.
    """
    def __init__(self, manager, mimetype: QMimeType):
        super().__init__()

        self.manager = manager
        self.mimetype = mimetype
        self.apps = None
        self.refresh(first_run=True)

    def refresh(self, first_run=False):
        self.apps = list(self.manager.get_supported_apps(self.mimetype.name()).items())
        if not first_run:
            self.dataChanged.emit(QModelIndex(), QModelIndex())

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

    def rowCount(self, _index):
        """
        Return list of rows in the model.
        """
        return len(self.apps)
