
import collections
import configparser
import itertools
import logging
import os
import pprint

from dataclasses import dataclass
from typing import List, Dict

from PyQt5.QtCore import Qt, QStandardPaths

SECTION_DEFAULTS = "Default Applications"
SECTION_ADDED = "Added Associations"
SECTION_REMOVED = "Removed Associations"
SECTION_MIME_CACHE = "MIME Cache"

@dataclass
class MimeAppChoiceSettings:
    """Represents details for a default application choice."""
    # Whether the entry is disabled via Removed Associations
    disabled: bool = False

    # Whether the entry is a custom association
    custom: bool = False

class MimeTypesManager():
    """
    Class to enumerate and manage default applications for MIME types.
    All functions in this class expect MIME types as strings instead of QMimeType instances.
    """
    def __init__(self, desktop_entries: str, *, paths: List[str] = None, cache_paths: List[str] = None) -> List[str]:
        self.desktop_entries = desktop_entries

        self.mimeapps_db = collections.defaultdict(dict)
        self.mimeapps_local = None
        self.mimeapps_local_path = None
        self.mimeinfo_cache = collections.defaultdict(list)

        self._initialize_mimeapps(paths=paths)
        self._initialize_mimeinfo_cache(paths=cache_paths)

    def _initialize_mimeapps(self, paths=None):
        """Initialize mimeapps.list database, which is used to manage preferred applications and custom associations."""
        if paths is None:
            # Use system wide + user specific mimeapps.list paths
            paths = self._get_mimeapps_list_paths()
            print("mimeapps.list paths:", self._get_mimeapps_list_paths())

        if not paths:
            # If no paths were found, use $XDG_CONFIG_HOME/mimeapps.list (~/.config/mimeapps.list)
            paths = [os.path.join(QStandardPaths.writableLocation(QStandardPaths.ConfigLocation), "mimeapps.list")]

        # For each location of mimeapps.list, merge the definitions into a single store
        # Since each section specifies a list, we can't use configparser's built-in handling of multiple files,
        # since that overrides already seen keys
        self.mimeapps_db.clear()
        for path in paths:
            loader = configparser.ConfigParser()
            loader.read(path)
            logging.debug("Reading mimeapps.list entries from %s", path)

            # Treat the first mimeapps.list path as the writable one. Usually this will be ~/.config/mimeapps.list
            if self.mimeapps_local is None:
                self.mimeapps_local = loader
                self.mimeapps_local_path = path
                logging.info("Setting write path to %s", path)

            for section in {SECTION_ADDED, SECTION_DEFAULTS, SECTION_REMOVED}:
                if loader.has_section(section):
                    db_section = self.mimeapps_db[section]
                    for key, value in loader[section].items():
                        value = value.strip(';').split(';')
                        existing = db_section.get(key, [])
                        db_section[key] = existing + value

    def _initialize_mimeinfo_cache(self, paths=None):
        """Initialize mimeinfo.cache store, which is used to map MIME apps to a list of programs that handle them.

        This file is also used to set fallback file associations if no default is set by mimeapps.list"""
        if not paths:
            paths = QStandardPaths.locateAll(QStandardPaths.ApplicationsLocation, "mimeinfo.cache")

        self.mimeinfo_cache.clear()
        for path in paths:
            loader = configparser.ConfigParser(strict=False)  # Ignore duplicates when parsing
            loader.read(path)
            logging.debug("Reading mimeinfo.cache entries from %s", path)
            if loader.has_section(SECTION_MIME_CACHE):
                for key, value in loader[SECTION_MIME_CACHE].items():
                    values = value.strip(';').split(';')
                    self.mimeinfo_cache[key] += values

    @staticmethod
    def _get_mimeapps_list_paths():
        """
        Returns a list of mimeapps.list paths, in order of decreasing priority.

        Based off of: https://specifications.freedesktop.org/mime-apps-spec/latest/ar01s02.html
        """
        current_desktops = os.environ.get('XDG_CURRENT_DESKTOP', '').split(':')

        user_defaults_per_desktop = list(itertools.chain.from_iterable(
            QStandardPaths.locateAll(QStandardPaths.ConfigLocation, f"{desktop}-mimeapps.list")
            for desktop in current_desktops
        ))
        user_defaults = QStandardPaths.locateAll(QStandardPaths.ConfigLocation, "mimeapps.list")

        global_defaults_per_desktop = list(itertools.chain.from_iterable(
            QStandardPaths.locateAll(QStandardPaths.ApplicationsLocation,
                                     f"{desktop}-mimeapps.list")
            for desktop in current_desktops
        ))
        global_defaults = QStandardPaths.locateAll(QStandardPaths.ApplicationsLocation, "mimeapps.list")
        return user_defaults_per_desktop + user_defaults + global_defaults_per_desktop + global_defaults

    def get_default_app(self, mimetype: str):
        """
        Returns the default application for the MIME type, or None if none is set.
        """
        default_entries = self.mimeapps_db[SECTION_DEFAULTS].get(mimetype, [])
        disabled_entries = self.mimeapps_db[SECTION_REMOVED].get(mimetype, [])
        for entry_id in default_entries:
            if entry_id in self.desktop_entries.entries and entry_id not in disabled_entries:
                return entry_id

        fallback_entries = self.mimeinfo_cache.get(mimetype, [])
        for entry_id in fallback_entries:
            if entry_id in self.desktop_entries.entries and entry_id not in disabled_entries:
                return entry_id
        return None  # Not found

    def _write(self):
        with open(self.mimeapps_local_path, 'w') as f:
            self.mimeapps_local.write(f, space_around_delimiters=False)

    def has_default(self, mimetype: str) -> bool:
        """Returns whether a default for the MIME type was explicitly set."""
        return mimetype in self.mimeapps_db[SECTION_DEFAULTS]

    def set_default_app(self, mimetype: str, app_id: str):
        """
        Sets the default application for the MIME type.
        """
        logging.debug("Setting app %s as default for %s", app_id, mimetype)
        self.mimeapps_db[SECTION_DEFAULTS][mimetype] = [app_id]
        self.mimeapps_local[SECTION_DEFAULTS][mimetype] = app_id
        self._write()

    def clear_default_app(self, mimetype: str):
        """
        Clears the user-defined default application for the MIME type.
        """
        logging.debug("Clearing default for %s", mimetype)
        try:
            current_default = self.mimeapps_local[SECTION_DEFAULTS][mimetype].strip(';')
            del self.mimeapps_local[SECTION_DEFAULTS][mimetype]
            self.mimeapps_db[SECTION_DEFAULTS][mimetype].remove(current_default)
        except (KeyError, IndexError):
            logging.warning("Tried to clear default app on mimetype %s when none was set", mimetype)
        else:
            self._write()

    def get_supported_apps(self, mimetype: str) -> Dict[str, MimeAppChoiceSettings]:
        """
        Returns a dict of apps (str to MimeAppChoiceSettings instances) that support a MIME type.

        This includes apps that support the type natively as well as custom associations added via mimeapps.list
        """
        disabled_apps = self.mimeapps_db[SECTION_REMOVED].get(mimetype, [])

        results = {}
        # Add all associations from .desktop entries (mimeinfo.cache)
        for app_id in self.mimeinfo_cache.get(mimetype, []):
            results[app_id] = MimeAppChoiceSettings(disabled=app_id in disabled_apps, custom=False)
        # Add all custom associations from mimeapps.list
        for app_id in self.mimeapps_db[SECTION_ADDED].get(mimetype, []):
            results[app_id] = MimeAppChoiceSettings(disabled=app_id in disabled_apps, custom=True)

        return results

    def add_association(self, mimetype: str, app_id: str):
        """
        STUB: Registers a new desktop entry to the MIME type.
        """
        return

    def disable_association(self, mimetype: str, app_id: str):
        return

    def enable_association(self, mimetype: str, app_id: str):
        return

    def remove_association(self, mimetype: str, app_id: str):
        return
