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
