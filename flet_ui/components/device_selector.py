"""Reusable Arduino/NI-DAQ selector."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass

import flet as ft

from components.mounting import update_if_mounted
from pydaq.core.acquisition import DeviceFamily
from theme import (
    ACCENT,
    ACTION_HEIGHT,
    BORDER,
    CONTROL_RADIUS,
    MUTED,
    NAVY,
    SURFACE,
    TEXT_LABEL,
)

FAMILY_LABELS = {DeviceFamily.ARDUINO: "Arduino", DeviceFamily.NIDAQ: "NI-DAQ"}

DeviceCallback = Callable[[DeviceFamily], None]


@dataclass(frozen=True)
class _FamilyButton:
    box: ft.Container
    radio_ring: ft.Container
    radio_dot: ft.Container
    label: ft.Text


class DeviceSelector(ft.Row):
    """Two-option hardware selector used above acquisition views."""

    def __init__(
        self,
        selected: DeviceFamily = DeviceFamily.ARDUINO,
        on_change: DeviceCallback | None = None,
    ) -> None:
        self.value = selected
        self._on_value_change = on_change
        self._buttons = {family: self._build_button(family) for family in DeviceFamily}
        super().__init__(
            controls=[button.box for button in self._buttons.values()],
            spacing=10,
            tight=True,
        )
        self._refresh_styles()

    def _build_button(self, family: DeviceFamily) -> _FamilyButton:
        radio_dot = ft.Container(width=10, height=10, border_radius=5)
        radio_ring = ft.Container(
            width=20,
            height=20,
            border_radius=10,
            alignment=ft.Alignment.CENTER,
            content=radio_dot,
        )
        label = ft.Text(FAMILY_LABELS[family], size=TEXT_LABEL, weight=ft.FontWeight.W_500)
        box = ft.Container(
            width=144,
            height=ACTION_HEIGHT,
            alignment=ft.Alignment.CENTER,
            border_radius=CONTROL_RADIUS,
            ink=True,
            on_click=lambda _event, choice=family: self.select(choice),
            content=ft.Row(
                controls=[radio_ring, label],
                spacing=9,
                tight=True,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
        )
        return _FamilyButton(box, radio_ring, radio_dot, label)

    def select(self, family: DeviceFamily) -> None:
        """Select a hardware family and notify the host page."""
        if family == self.value:
            return
        self.value = family
        self._refresh_styles()
        update_if_mounted(self)
        if self._on_value_change is not None:
            self._on_value_change(family)

    def _refresh_styles(self) -> None:
        for family, button in self._buttons.items():
            selected = family == self.value
            button.box.bgcolor = ACCENT if selected else SURFACE
            button.box.border = ft.Border.all(width=1, color=ACCENT if selected else BORDER)
            button.radio_ring.border = ft.Border.all(
                width=2, color=ft.Colors.WHITE if selected else MUTED
            )
            button.radio_dot.bgcolor = ft.Colors.WHITE if selected else None
            button.label.color = ft.Colors.WHITE if selected else NAVY
