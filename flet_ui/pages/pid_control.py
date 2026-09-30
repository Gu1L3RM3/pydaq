"""PID Control route."""

from __future__ import annotations

import flet as ft

from pages.placeholder import build_placeholder_page


def build_pid_control_page() -> ft.Control:
    return build_placeholder_page("PID Control", "Configure the PID controller.")
