"""Device and AI/AO channel fields shared by every hardware workflow."""

from __future__ import annotations

from dataclasses import dataclass

import flet as ft

from components.forms.choices import ChannelPicker
from components.forms.fields import LabeledDropdown
from theme import FORM_GAP


@dataclass(frozen=True)
class ChannelOptions:
    available: tuple[str, ...]
    selected: tuple[str, ...]


@dataclass(frozen=True)
class DeviceChoices:
    """What a device family offers; ``None`` channels hide that picker."""

    devices: tuple[str, ...]
    ai_channels: ChannelOptions | None = None
    ao_channels: ChannelOptions | None = None

    def __post_init__(self) -> None:
        if not self.devices:
            raise ValueError("devices must list at least one device label")


class DeviceSection(ft.Column):
    """Device dropdown plus optional AI and AO channel pickers.

    Example (Step Response needs both directions)::

        DeviceSection(DeviceChoices(
            ("COM3 · Arduino Uno",),
            ai_channels=ChannelOptions(("A0", "A1"), ("A0",)),
            ao_channels=ChannelOptions(("D9",), ("D9",)),
        ))
    """

    def __init__(self, choices: DeviceChoices) -> None:
        self._choices = choices
        self.device = LabeledDropdown("Device", choices.devices, choices.devices[0])
        self.ai_picker = _optional_picker("AI channels", choices.ai_channels)
        self.ao_picker = _optional_picker("AO channels", choices.ao_channels)
        pickers = [picker for picker in (self.ai_picker, self.ao_picker) if picker]
        super().__init__(
            controls=[self.device, *pickers],
            spacing=FORM_GAP,
            horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
        )

    @property
    def device_label(self) -> str:
        return self.device.value

    @property
    def ai_channels(self) -> tuple[str, ...]:
        return self.ai_picker.value if self.ai_picker else ()

    @property
    def ao_channels(self) -> tuple[str, ...]:
        return self.ao_picker.value if self.ao_picker else ()

    def set_choices(self, choices: DeviceChoices) -> None:
        """Swap options, e.g. on a device family change; pickers cannot appear later."""
        if _shape(choices) != _shape(self._choices):
            raise ValueError(
                f"choices must keep the same AI/AO pickers {_shape(self._choices)}, "
                f"received {_shape(choices)}"
            )
        self._choices = choices
        self.device.set_options(choices.devices, choices.devices[0])
        _reset_picker(self.ai_picker, choices.ai_channels)
        _reset_picker(self.ao_picker, choices.ao_channels)


def _optional_picker(label: str, options: ChannelOptions | None) -> ChannelPicker | None:
    if options is None:
        return None
    return ChannelPicker(label, options.available, options.selected)


def _reset_picker(picker: ChannelPicker | None, options: ChannelOptions | None) -> None:
    if picker is None or options is None:
        return
    picker.set_options(options.available, options.selected)


def _shape(choices: DeviceChoices) -> tuple[bool, bool]:
    return (choices.ai_channels is not None, choices.ao_channels is not None)
