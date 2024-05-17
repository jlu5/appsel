"""
Styled item delegates: these provide custom formatting for views.
"""
from PyQt5.QtWidgets import QStyledItemDelegate

class DefaultAppOptionsDelegate(QStyledItemDelegate):
    """
    Provides custom styling for the default app chooser list view.
    """
    def __init__(self, model, attr):
        super().__init__()
        self.model = model
        self.attr = attr

    def initStyleOption(self, option, index):
        """
        Override styling options for applications in SelectDefaultAppDialog:

        - Strike out disabled apps
        - Italicize custom associations
        - Bold the current default app
        """
        super().initStyleOption(option, index)
        _app_id, options = getattr(self.model, self.attr)[index.row()]
        option.font.setStrikeOut(options.disabled)
        option.font.setItalic(options.custom)
        option.font.setBold(options.default)

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
