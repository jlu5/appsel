from PyQt5.QtCore import (
    QModelIndex,
    QSortFilterProxyModel
)

class FilteredAppsListModel(QSortFilterProxyModel):
    """
    Custom QSortFilterProxyModel filtering based on search query, and applications that have at least one
    supported file type.
    """
    def __init__(self, parent, manager, ui):
        super().__init__(parent)
        self.manager = manager
        self.ui = ui

    def filterAcceptsRow(self, sourceRow: int, sourceParent: QModelIndex):
        searchQuery = super().filterAcceptsRow(sourceRow, sourceParent)

        app_id = self.sourceModel().apps[sourceRow]
        supported_types = self.manager.get_supported_types(app_id)
        if not supported_types and not self.ui.showAllAppsCheckBox.checkState():
            return False

        return searchQuery
