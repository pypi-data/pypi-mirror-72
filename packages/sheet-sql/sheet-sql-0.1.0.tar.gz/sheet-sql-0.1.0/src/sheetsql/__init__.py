"""SQL for Google Sheets."""
try:
    from importlib.metadata import version, PackageNotFoundError  # type: ignore
except ImportError:  # pragma: no cover
    from importlib_metadata import version, PackageNotFoundError  # type: ignore
from typing import Any

from .connection import GoogleSheetsConnection

try:
    __version__ = version(__name__)
except PackageNotFoundError:
    __version__ = "unknown"


def connect(auth_type: str, **kwargs: Any) -> GoogleSheetsConnection:
    """Connect to Google Sheets via gspread oauth or service_account."""
    return GoogleSheetsConnection(auth_type, **kwargs)
