"""Reusable Arduino/NI-DAQ selector."""

from __future__ import annotations

from collections.abc import Callable

import flet as ft

from pydaq.core.acquisition import DeviceFamily
from theme import ACCENT, BORDER, CONTROL_RADIUS, MUTED, NAVY, SURFACE

FAMILY_LABELS = {DeviceFamily.ARDUINO: "Arduino", DeviceFamily.NIDAQ: "NI-DAQ"}

DeviceCallback = Callable[[DeviceFamily], None]


class DeviceSelector(ft.Row):
    """Two-option hardware selector used above acquisition views."""

    def __init__(
        self,
        selected: DeviceFamily = DeviceFamily.ARDUINO,
        on_change: DeviceCallback | None = None,
    ) -> None:
        self.value = selected
        self._on_value_change = on_change
        self._buttons = {
            family: self._build_button(family) for family in DeviceFamily
        }
        super().__init__(
            controls=list(self._buttons.values()),
            spacing=10,
            tight=True,
        )
        self._refresh_styles()

    def _build_button(self, family: DeviceFamily) -> ft.Container:
        return ft.Container(
            width=144,
            height=44,
            alignment=ft.Alignment.CENTER,
            border_radius=CONTROL_RADIUS,
            border=ft.Border.all(width=1, color=BORDER),
            ink=True,
            on_click=lambda _event, choice=family: self.select(choice),
            content=ft.Row(
                controls=[
                    ft.Container(
                        width=20,
                        height=20,
                        border_radius=10,
                        border=ft.Border.all(width=2, color=MUTED),
                        alignment=ft.Alignment.CENTER,
                        content=ft.Container(width=10, height=10, border_radius=5),
                    ),
                    ft.Text(FAMILY_LABELS[family], size=14, weight=ft.FontWeight.W_500),
                ],
                spacing=9,
                tight=True,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
        )

    def select(self, family: DeviceFamily) -> None:
        """Select a hardware family and notify the host page."""
        if family == self.value:
            return
        self.value = family
        self._refresh_styles()
        self.update()
        if self._on_value_change is not None:
            self._on_value_change(family)

    def _refresh_styles(self) -> None:
        for family, button in self._buttons.items():
            selected = family == self.value
            button.bgcolor = ACCENT if selected else SURFACE
            button.border = ft.Border.all(width=1, color=ACCENT if selected else BORDER)
            content = button.content
            if not isinstance(content, ft.Row):
                continue
            radio, label = content.controls
            if isinstance(radio, ft.Container):
                radio.border = ft.Border.all(
                    width=2, color=ft.Colors.WHITE if selected else MUTED
                )
                if isinstance(radio.content, ft.Container):
                    radio.content.bgcolor = ft.Colors.WHITE if selected else None
            if isinstance(label, ft.Text):
                label.color = ft.Colors.WHITE if selected else NAVY
