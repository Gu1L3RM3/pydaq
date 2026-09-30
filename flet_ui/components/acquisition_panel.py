"""Reusable acquisition settings panel."""

from __future__ import annotations

from collections.abc import Callable

import flet as ft

from components.device_selector import DeviceFamily
from components.form_controls import (
    ChoiceTabs,
    LabeledDropdown,
    LabeledNumberField,
    PathField,
    ToggleSetting,
)
from components.panel import PanelCard
from theme import ACCENT, ACCENT_DARK, BORDER, CONTROL_RADIUS

AcquisitionCallback = Callable[[bool], None]


class AcquisitionSetupPanel(PanelCard):
    """Device settings and primary acquisition action."""

    def __init__(self, on_acquisition_change: AcquisitionCallback | None = None) -> None:
        self._on_acquisition_change = on_acquisition_change
        self._running = False
        self.device = LabeledDropdown(
            "Device",
            options=("COM3 · Arduino Uno", "COM4 · Arduino Mega"),
            value="COM3 · Arduino Uno",
        )
        self.channels = LabeledDropdown(
            "AI channels", options=("A0, A1", "A0", "A1"), value="A0, A1"
        )
        self._action_icon = ft.Icon(ft.Icons.PLAY_ARROW_ROUNDED, color=ft.Colors.WHITE)
        self._action_label = ft.Text(
            "Start acquisition",
            color=ft.Colors.WHITE,
            size=15,
            weight=ft.FontWeight.W_600,
        )
        self._action = ft.Container(
            height=44,
            bgcolor=ACCENT,
            border_radius=CONTROL_RADIUS,
            alignment=ft.Alignment.CENTER,
            ink=True,
            on_click=self._toggle_acquisition,
            content=ft.Row(
                controls=[self._action_icon, self._action_label],
                spacing=8,
                tight=True,
            ),
        )
        form = ft.Column(
            controls=[
                self.device,
                self.channels,
                LabeledNumberField("Sample period (s)", "0.010"),
                LabeledNumberField("Session duration (s)", "100"),
                ToggleSetting("Digital filter?"),
                ft.Row(
                    controls=[
                        ft.Text("Plot data?", size=14, weight=ft.FontWeight.W_500),
                        ft.Container(
                            content=ChoiceTabs(
                                ("Real time", "At the end", "Off"), "Real time"
                            ),
                            expand=True,
                        ),
                    ],
                    spacing=12,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                ToggleSetting("Save data?"),
                PathField("~/Documents/PYDAQ"),
                ft.Divider(height=4, color=BORDER),
                self._action,
            ],
            spacing=3,
            horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
        )
        super().__init__(
            form,
            title="Acquisition setup",
            description="Configure your device and acquisition parameters.",
            padding=14,
            header_gap=4,
        )

    def set_device_family(self, family: DeviceFamily) -> None:
        """Apply family-specific device and channel options."""
        if family is DeviceFamily.ARDUINO:
            self.device.set_options(
                ("COM3 · Arduino Uno", "COM4 · Arduino Mega"),
                "COM3 · Arduino Uno",
            )
            self.channels.set_options(("A0, A1", "A0", "A1"), "A0, A1")
            return
        self.device.set_options(("Dev1 · NI USB-6009", "Dev2 · NI-DAQ"), "Dev1 · NI USB-6009")
        self.channels.set_options(("ai0, ai1", "ai0", "ai1"), "ai0, ai1")

    def _toggle_acquisition(self, _event: ft.Event[ft.Container]) -> None:
        self._running = not self._running
        self._action_icon.icon = (
            ft.Icons.STOP_ROUNDED if self._running else ft.Icons.PLAY_ARROW_ROUNDED
        )
        self._action_label.value = (
            "Stop acquisition" if self._running else "Start acquisition"
        )
        self._action.bgcolor = ACCENT_DARK if self._running else ACCENT
        self.update()
        if self._on_acquisition_change is not None:
            self._on_acquisition_change(self._running)
