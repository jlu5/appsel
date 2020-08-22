
# pylint: disable=invalid-name
from PyQt5.QtCore import Qt, QAbstractTableModel, QMimeDatabase, QModelIndex, QVariant

from appsel.backend import utils

class DefaultsForAppModel(QAbstractTableModel):
    """
    Represents a list of MIME types that an application supports.
    """

    COLUMNS = ["MIME Type", "Status", "File Extensions"]

    def __init__(self, manager, app_id: str):
        super().__init__()

        self.manager = manager
        self.app_id = app_id
        self.refresh(first_run=True)

    def refresh(self, first_run=False):
        self.supported_types = list(self.manager.get_supported_types(self.app_id).items())
        self.supported_types.sort(key=lambda item: item[0].casefold())
        if not first_run:
            self.dataChanged.emit(QModelIndex(), QModelIndex())

    def data(self, index, role):
        accessors = [self._get_mimetype, self._get_status, self._get_extensions]
        try:
            return accessors[index.column()](index, role)
        except IndexError:
            return QVariant()

    def _get_mimetype(self, index, role):
        """
        Return a list of MIME types that the app supports.
        """
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
            # A MIME type is:
            # - Checked if the app is explicitly set as default for that type
            # - Partial if it was implicitly set as default
            # - Unchecked otherwise
            if self.manager.get_default_app(mimetype) == self.app_id:
                if self.manager.has_default(mimetype):
                    return Qt.Checked
                else:
                    return Qt.PartiallyChecked
            else:
                return Qt.Unchecked
        return QVariant()

    def _get_extensions(self, index, role):
        """Returns display data for the File Extensions column."""
        mimetype, _options = self.supported_types[index.row()]
        qm = self.manager.qmimedb.mimeTypeForName(mimetype)
        if role == Qt.DisplayRole:
            return ",".join(qm.suffixes())
        return QVariant()

    def _get_status(self, index, role):
        """Returns display data for the Status column."""
        mimetype, _options = self.supported_types[index.row()]
        if role == Qt.DisplayRole:
            return "User defined" if self.manager.has_default(mimetype) else "Automatic"
        return QVariant()

    def setData(self, index, value, role):
        """
        Update the checked state for a MIME type.
        """
        if not index.isValid() or role != Qt.CheckStateRole:
            return False
        if index.column() != 0:
            return False

        mimetype, options = self.supported_types[index.row()]
        if value == Qt.Checked:
            self.manager.set_default_app(mimetype, self.app_id)
        else:
            self.manager.clear_default_app(mimetype)
        options.default = self.manager.get_default_app(mimetype) == self.app_id
        # Refresh the entire row so that other sections like Status update
        self.dataChanged.emit(index, index.sibling(index.row(), len(self.COLUMNS)-1))
        return True

    def headerData(self, section, orientation, role):
        if role == Qt.DisplayRole and orientation == Qt.Horizontal:
            return self.COLUMNS[section]
        return QVariant()

    def flags(self, index):
        """
        Return Qt item flags for the given index.
        """
        default_flags = super().flags(index)
        if index.isValid() and index.column() == 0:
            return default_flags | Qt.ItemIsUserCheckable
        return default_flags

    def rowCount(self, _index):
        """
        Return list of rows in the model.
        """
        return len(self.supported_types)

    def columnCount(self, _index):
        """
        Return list of columns in the model.
        """
        return len(self.COLUMNS)
