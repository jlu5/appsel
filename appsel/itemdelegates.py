"""
Styled item delegates: these provide custom formatting for views.
"""
from PyQt5.QtWidgets import QStyledItemDelegate

class MimeTypesListDelegate(QStyledItemDelegate):
    def __init__(self, manager, source_model, filtered_model):
        super().__init__()
        self.manager = manager
        self.source_model = source_model
        self.filtered_model = filtered_model

    def initStyleOption(self, option, index):
        """Paint handler: bold every row where the default application has been set."""
        super().initStyleOption(option, index)
        source_index = self.filtered_model.mapToSource(index)
        mimetype = self.source_model.mimetypes[source_index.row()]
        if self.manager.has_default(mimetype.name()):
            option.font.setBold(True)
