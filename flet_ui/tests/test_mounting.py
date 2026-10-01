"""Tests for mount-safe control updates."""

from __future__ import annotations

import flet as ft

from components.mounting import is_mounted, update_if_mounted


def test_unmounted_control_is_not_updated() -> None:
    text = ft.Text("idle")

    update_if_mounted(text)

    assert is_mounted(text) is False
