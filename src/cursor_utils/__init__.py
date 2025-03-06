"""Cursor Utils - A modern CLI utility toolkit for Cursor."""

from importlib import metadata

try:
    __version__ = metadata.version(__name__)
except metadata.PackageNotFoundError:  # pragma: no cover
    __version__ = "unknown"

__all__ = ["__version__"]
