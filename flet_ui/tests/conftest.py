"""Test configuration for the script-oriented Flet application."""

from __future__ import annotations

import sys
from pathlib import Path

FLET_UI_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(FLET_UI_ROOT))
