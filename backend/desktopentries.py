import collections
import logging
import os
import os.path

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

        # Map MIME types to applications that support it
        self.mimemap = collections.defaultdict(list)
        for name, path in self.desktop_entry_paths.items():
            self.entries[name] = entry = xdg.DesktopEntry.DesktopEntry(filename=path)
            for mimetype in entry.getMimeTypes():
                self.mimemap[mimetype].append(name)

    def get_mimetypes(self, desktop_entry_id: str) -> List[str]:
        """Returns the MIME types supported by a desktop entry."""
        return self.entries[desktop_entry_id].getMimeTypes()

    def get_applications(self, mimetype: str) -> List[str]:
        """
        Returns the applications registered for a given MIME type.
        """
        return self.mimemap.get(mimetype, [])

    def get_name(self, desktop_entry_id: str) -> str:
        """Returns the name of a desktop entry, if it exists."""
        return self.entries[desktop_entry_id].getName()

    def get_icon(self, desktop_entry_id: str) -> QIcon:
        """Returns a QIcon representing a desktop entry, if it exists."""
        entry = self.entries[desktop_entry_id]
        # Icon definitions in .desktop entries can be a name (icon pulled from the current icon theme)
        # or an absolute path.
        iconname = entry.getIcon()
        if os.path.isabs(iconname):
            return QIcon.QIcon(iconname)
        else:
            return QIcon.fromTheme(iconname)

    def is_shown(self, desktop_entry_id: str) -> bool:
        """
        Returns whether the desktop entry should be shown in the applications list.

        Apps are displayed if they meet the following criteria:
        1) Desktop entry is not marked NoDisplay or Hidden
        2) The desktop entry supports at least 1 mime type
        3) The OnlyShowIn and NotShowIn criteria are met for the desktop entry
        4) The path pointed to by TryExec exists, if the field exists
        """
        entry = self.entries[desktop_entry_id]

        if entry.getHidden() or entry.getNoDisplay():
            return False

        if not entry.getMimeTypes():
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
        if tryexec and not os.path.exists(tryexec):
            logging.debug("Not showing desktop entry %s because TryExec path %s does not exist",
                            desktop_entry_id, tryexec)
            return False
        return True
