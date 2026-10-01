"""Helpers for controls that may be updated before mount or after unmount."""

from __future__ import annotations

import flet as ft


def is_mounted(control: ft.BaseControl) -> bool:
    """Whether ``control`` is attached to a page.

    Flet 1.0 raises ``RuntimeError`` from ``control.page`` instead of returning
    ``None``, and worker-thread callbacks can arrive after navigation.
    """
    try:
        control.page
    except RuntimeError:
        return False
    return True


def update_if_mounted(control: ft.BaseControl) -> None:
    """Refresh ``control`` on screen; state changes before mount render later."""
    if is_mounted(control):
        control.update()
