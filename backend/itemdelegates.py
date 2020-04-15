from PyQt5.QtWidgets import QStyledItemDelegate

class MimeTypesListDelegate(QStyledItemDelegate):
    def __init__(self, model):
        super().__init__()
        self.model = model
        self.manager = model.manager

    def paint(self, painter, option, index):
        """Paint handler: bold every row where the default application has been set."""
        mimetype = self.model.mimetypes[index.row()]
        if self.manager.has_default(mimetype.name()):
            option.font.setBold(True)

        return super().paint(painter, option, index)
