"""Reusable acquisition settings panel."""

from __future__ import annotations

from collections.abc import Callable

import flet as ft

from components.forms.choices import ChoiceTabs, ToggleSetting
from components.forms.fields import LabeledDropdown, LabeledNumberField, PathField
from components.panel import PanelCard
from pydaq.core.acquisition import AcquisitionConfig, DeviceFamily
from services.acquisition_form import build_acquisition_config
from theme import ACCENT, ACCENT_DARK, BORDER, CONTROL_RADIUS

AcquisitionCallback = Callable[[bool], None]


class AcquisitionSetupPanel(PanelCard):
    """Device settings and primary acquisition action.

    The action button only requests a change through ``on_acquisition_change``;
    the host confirms it with ``set_running`` once the session starts or ends.
    """

    def __init__(self, on_acquisition_change: AcquisitionCallback | None = None) -> None:
        self._on_acquisition_change = on_acquisition_change
        self._running = False
        self._family = DeviceFamily.ARDUINO
        self.device = LabeledDropdown(
            "Device",
            options=("COM3 · Arduino Uno", "COM4 · Arduino Mega"),
            value="COM3 · Arduino Uno",
        )
        self.channels = LabeledDropdown(
            "AI channels", options=("A0, A1", "A0", "A1"), value="A0, A1"
        )
        self.sample_period = LabeledNumberField("Sample period (s)", "0.010")
        self.duration = LabeledNumberField("Session duration (s)", "100")
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
                self.sample_period,
                self.duration,
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
            spacing=13,
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
        self._family = family
        if family is DeviceFamily.ARDUINO:
            self.device.set_options(
                ("COM3 · Arduino Uno", "COM4 · Arduino Mega"),
                "COM3 · Arduino Uno",
            )
            self.channels.set_options(("A0, A1", "A0", "A1"), "A0, A1")
            return
        self.device.set_options(("Dev1 · NI USB-6009", "Dev2 · NI-DAQ"), "Dev1 · NI USB-6009")
        self.channels.set_options(("ai0, ai1", "ai0", "ai1"), "ai0, ai1")

    def read_config(self) -> AcquisitionConfig:
        """Return the form as a config; raises ``ValueError`` with a user message."""
        return build_acquisition_config(
            self._family,
            self.device.value,
            self.channels.value,
            self.sample_period.value,
            self.duration.value,
        )

    def set_running(self, running: bool) -> None:
        """Show the start or stop action without notifying the host."""
        self._running = running
        self._action_icon.icon = (
            ft.Icons.STOP_ROUNDED if running else ft.Icons.PLAY_ARROW_ROUNDED
        )
        self._action_label.value = "Stop acquisition" if running else "Start acquisition"
        self._action.bgcolor = ACCENT_DARK if running else ACCENT
        self.update()

    def _toggle_acquisition(self, _event: ft.Event[ft.Container]) -> None:
        if self._on_acquisition_change is not None:
            self._on_acquisition_change(not self._running)
