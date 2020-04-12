import collections
import os
import os.path

import xdg.DesktopEntry
from PyQt5.QtCore import QStandardPaths

class DesktopEntriesList():
    """Enumerate and provide display information for .desktop entries on the system."""

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
