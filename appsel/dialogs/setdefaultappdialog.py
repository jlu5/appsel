#!/usr/bin/env python3
import enum
import logging

from PyQt5.QtWidgets import QDialog
from PyQt5.uic import loadUi

from .addcustomappdialog import AddCustomAppDialog  # pylint: disable=relative-beyond-top-level
from appsel.backend.models.defaultappoptionsmodel import DefaultAppOptionsModel

class ToggleApplicationAction(enum.Enum):
    """Represents the action taken by the Disable / Enable / Remove application button."""
    DISABLE = 0
    ENABLE = 1
    REMOVE = 2

class SetDefaultAppDialog(QDialog):
    """
    Dialog to select the default application for a MIME type.
    """
    uifile = "ui/setdefaultappdialog.ui"
    def __init__(self, mimetypemanager, mimetype: str, parent=None):
        super().__init__()
        self._app = parent
        self.manager = mimetypemanager
        self.mimetype = mimetype
        logging.debug('Launching SetDefaultAppDialog for %s', mimetype)

        self.model = DefaultAppOptionsModel(self.manager, mimetype)

        # Selection state
        self.current_index = None
        self.current_toggle_option = None

        self._ui = loadUi(self.uifile, self)
        # XXX: internationalize
        self._ui.setWindowTitle(f"Set default application for {mimetype}")
        # Buttons
        self._ui.addApplication.clicked.connect(self.on_add_application)
        self._ui.toggleApplication.clicked.connect(self.on_toggle_application)
        self._ui.setAsDefault.clicked.connect(self.on_set_default)
        # ListView
        self._ui.appsView.setModel(self.model)
        self._ui.appsView.selectionModel().selectionChanged.connect(self.on_row_changed)
        self._ui.show()

    def _update_toggle_action(self):
        """Update the action pointed to by the toggle / remove application button."""
        if self.current_index is None:
            self.current_toggle_option = None
            return

        _app_id, options = self.model.apps[self.current_index]
        # XXX: internationalize text strings
        if options.disabled:
            self.current_toggle_option = ToggleApplicationAction.ENABLE
            self._ui.toggleApplication.setText("Enable application")
        elif options.custom:
            self.current_toggle_option = ToggleApplicationAction.REMOVE
            self._ui.toggleApplication.setText("Remove application")
        else:
            self.current_toggle_option = ToggleApplicationAction.DISABLE
            self._ui.toggleApplication.setText("Disable application")

    def on_row_changed(self, selected, _deselected):
        if selected.indexes():
            self.current_index = selected.indexes()[0].row()
            self._update_toggle_action()

    def on_add_application(self, _event):
        dlg = AddCustomAppDialog(self.manager.desktop_entries)
        if dlg.exec_():
            self.manager.add_association(self.mimetype, dlg.get_selected_app())
            self._refresh()

    def _refresh(self):
        self.model.refresh()
        if self._app:
            self._app.refresh()

    def on_set_default(self, _event):
        """Button handler: set or clear the default application."""
        if self.current_index is not None:
            app_id, _options = self.model.apps[self.current_index]

            # Clear the default app if it matches the system default
            if app_id == self.manager.get_default_app(self.mimetype, use_fallback=False):
                self.manager.clear_default_app(self.mimetype)
            else:
                self.manager.set_default_app(self.mimetype, app_id)
            self._refresh()

    def on_toggle_application(self, _event):
        """Button handler: enable, disable, or remove the application from the handlers for a file type."""
        if self.current_index is None:
            return

        app_id, _options = self.model.apps[self.current_index]
        if self.current_toggle_option is ToggleApplicationAction.ENABLE:
            self.manager.enable_association(self.mimetype, app_id)
        elif self.current_toggle_option is ToggleApplicationAction.DISABLE:
            self.manager.disable_association(self.mimetype, app_id)
        elif self.current_toggle_option is ToggleApplicationAction.REMOVE:
            self.manager.remove_association(self.mimetype, app_id)
            self.current_index = None
        else:
            logging.warning("Cannot toggle / remove application: current toggle option is not set: %s",
                            self.current_toggle_option, exc_info=True)
        self._refresh()
        self._update_toggle_action()
