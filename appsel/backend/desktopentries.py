import logging
import os
import os.path
import shutil

from typing import List

import xdg.DesktopEntry
from PyQt5.QtCore import QStandardPaths
from PyQt5.QtGui import QIcon

class DesktopEntriesList():
    """
    Enumerate and provide display information for .desktop entries on the system.
    All functions in this class expect MIME types as strings instead of QMimeType instances.
    """

    def __init__(self):
        self.entries = {}

        # For each .desktop entry in any path they are read from (~/.local/share/applications,
        # /usr/local/share/applications, /usr/share/applications), read only the highest priority
        # path for the desktop entry ID
        self.desktop_entry_paths = {}
        for location in QStandardPaths.standardLocations(QStandardPaths.ApplicationsLocation):
            for root, _dirs, files in os.walk(location):
                for filename in files:
                    if os.path.splitext(filename)[1] == '.desktop' and filename not in self.desktop_entry_paths:
                        fullpath = os.path.join(root, filename)
                        self.desktop_entry_paths[filename] = fullpath
                        print(f'Registered {filename} to {fullpath}')

        for name, path in self.desktop_entry_paths.items():
            self.entries[name] = xdg.DesktopEntry.DesktopEntry(filename=path)

    def get_mimetypes(self, desktop_entry_id: str) -> List[str]:
        """Returns the MIME types supported by a desktop entry."""
        try:
            return self.entries[desktop_entry_id].getMimeTypes()
        except KeyError:
            return []

    def get_name(self, desktop_entry_id: str) -> str:
        """Returns the name of a desktop entry, if it exists."""
        try:
            return self.entries[desktop_entry_id].getName()
        except KeyError:
            return desktop_entry_id

    def get_icon(self, desktop_entry_id: str) -> QIcon or None:
        """Returns a QIcon representing a desktop entry, if it exists."""
        try:
            entry = self.entries[desktop_entry_id]
        except KeyError:
            return None

        # Icon definitions in .desktop entries can be a name (icon pulled from the current icon theme)
        # or an absolute path.
        iconname = entry.getIcon()
        if os.path.isabs(iconname):
            return QIcon(iconname)
        else:
            return QIcon.fromTheme(iconname)

    def is_shown(self, desktop_entry_id: str) -> bool:
        """
        Returns whether the desktop entry should be shown in the applications list.

        Apps are displayed if they meet the following criteria:
        1) Desktop entry is not marked NoDisplay or Hidden
        2) The OnlyShowIn and NotShowIn criteria are met for the desktop entry
        3) The path pointed to by TryExec exists, if the field exists
        """
        try:
            entry = self.entries[desktop_entry_id]
        except KeyError:
            return False

        if entry.getHidden() or entry.getNoDisplay():
            return False

        current_desktops = set(os.environ.get('XDG_CURRENT_DESKTOP', '').split(':'))
        onlyshowin = entry.getOnlyShowIn()
        if onlyshowin and not set(onlyshowin) & current_desktops:
            logging.debug("Not showing desktop entry %s because %s does not match %s",
                          desktop_entry_id, current_desktops, onlyshowin)
            return False
        notshowin = entry.getNotShowIn()
        if notshowin and set(notshowin) & current_desktops:
            logging.debug("Not showing desktop entry %s because %s matches %s",
                          desktop_entry_id, current_desktops, notshowin)
            return False

        tryexec = entry.getTryExec()
        if tryexec:
            if not os.path.isabs(tryexec):
                # tryexec path can be absolute or relative
                tryexec = shutil.which(tryexec)
            if tryexec is None or not os.path.exists(tryexec):
                logging.debug("Not showing desktop entry %s because TryExec path %s does not exist",
                            desktop_entry_id, tryexec)
                return False
        return True
