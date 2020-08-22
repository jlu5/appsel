"""
Misc utility functions.
"""
from PyQt5.QtCore import QMimeType
from PyQt5.QtGui import QIcon

_ICON_CACHE = {}
def get_mimetype_icon(mimetype: QMimeType) -> QIcon:
    """
    Return a QIcon for the given QMIMEType.
    """
    if mimetype in _ICON_CACHE:
        return _ICON_CACHE[mimetype]
    else:
        # Show the icon for the MIME type, falling back to the generic type icon
        # or the "unknown type" icon if it's missing in the current icon theme
        fallback_unknown = QIcon.fromTheme("unknown")
        fallback_generic = QIcon.fromTheme(mimetype.genericIconName(), fallback_unknown)
        _ICON_CACHE[mimetype] = icon = QIcon.fromTheme(mimetype.iconName(), fallback_generic)
        return icon
