"""Compatibility path for ``from pydaq.pydaq_global import PydaqGui``."""

from pydaq.legacy_qt.app import PYDAQ_Global_GUI, PydaqGui

__all__ = ["PYDAQ_Global_GUI", "PydaqGui"]
