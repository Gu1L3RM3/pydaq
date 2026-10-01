"""Send Data setup panel composed from the shared setup sections."""

from __future__ import annotations

from collections.abc import Callable, Mapping

import flet as ft

from components.forms.buttons import ClickCallback, PrimaryActionButton
from components.forms.choices import LabeledChoice, format_channels
from components.forms.fields import LabeledNumberField, PathField
from components.mounting import update_if_mounted
from components.setup.device_section import DeviceChoices, DeviceSection
from components.setup.output_section import PLOT_MODES
from components.setup.setup_panel import SetupPanel
from components.setup.timing_section import TimingSection
from pydaq.core.acquisition import DeviceFamily
from services.send_form import SendRequest, build_send_request
from theme import ACCENT_DARK, FORM_GAP, MUTED, SPACE_SM, TEXT_CAPTION

SendCallback = Callable[[bool], None]

DEFAULT_DATA_FILE = "~/Desktop/data.dat"
REAL_TIME_PLOT = PLOT_MODES[0]

# What each family does with the file values, as the legacy widgets did.
_OUTPUT_NOTES = {
    DeviceFamily.ARDUINO: "Digital outputs: values above 2.5 V become HIGH (5 V).",
    DeviceFamily.NIDAQ: "Analog outputs: every value must fit the output range.",
}
_REAL_TIME_WARNING = (
    "Real-time plotting can delay sample periods below 0.05 s; "
    "plot at the end for fast signals."
)


def _note(icon: ft.IconData, text: str, color: str) -> tuple[ft.Row, ft.Text]:
    """Small icon + caption row; the text is returned so it can change later."""
    label = ft.Text(text, size=TEXT_CAPTION, color=color, expand=True)
    row = ft.Row(
        controls=[ft.Icon(icon, size=16, color=color), label],
        spacing=SPACE_SM,
        vertical_alignment=ft.CrossAxisAlignment.START,
    )
    return row, label


class OutputRangeFields(ft.Row):
    """NI-DAQ analog output limits side by side."""

    def __init__(self, minimum: str = "0", maximum: str = "5") -> None:
        self.minimum = LabeledNumberField("Output min (V)", minimum)
        self.maximum = LabeledNumberField("Output max (V)", maximum)
        self.minimum.expand = True
        self.maximum.expand = True
        super().__init__(controls=[self.minimum, self.maximum], spacing=SPACE_SM)

    @property
    def value(self) -> tuple[str, str]:
        return (self.minimum.value, self.maximum.value)


class SendSetupPanel(SetupPanel):
    """Device, data file, timing and plot settings plus the send action.

    Like ``AcquisitionSetupPanel``, the action only requests a change through
    ``on_send_change``; the host confirms it with ``set_running``.
    ``choices_by_family`` must offer AO channels for every family.
    """

    def __init__(
        self,
        choices_by_family: Mapping[DeviceFamily, DeviceChoices],
        on_send_change: SendCallback | None = None,
        on_browse: ClickCallback | None = None,
        family: DeviceFamily = DeviceFamily.ARDUINO,
    ) -> None:
        self._choices_by_family = choices_by_family
        self._family = family
        self.device = DeviceSection(choices_by_family[family])
        self.data_file = PathField(DEFAULT_DATA_FILE, on_browse, label="Data file")
        self._output_note, self._output_note_text = _note(
            ft.Icons.INFO_OUTLINE_ROUNDED, _OUTPUT_NOTES[family], MUTED
        )
        self.timing = TimingSection(sample_period="1.0", duration=None)
        self.output_range = OutputRangeFields()
        self.plot_mode = LabeledChoice(
            "Plot data?", PLOT_MODES, REAL_TIME_PLOT, on_change=self._show_plot_warning
        )
        self._plot_warning, _ = _note(
            ft.Icons.WARNING_AMBER_ROUNDED, _REAL_TIME_WARNING, ACCENT_DARK
        )
        self._action = PrimaryActionButton(
            "Send data",
            "Stop sending",
            on_toggle=on_send_change,
            idle_icon=ft.Icons.SEND_ROUNDED,
        )
        super().__init__(
            "Send setup",
            "Choose the output channels and the signal to replay.",
            # Same order as the acquisition setup: device, timing, options, then
            # the file path just above the action.
            sections=(
                self.device,
                self.timing,
                self.output_range,
                _group(self.plot_mode, self._plot_warning),
                _group(self.data_file, self._output_note),
            ),
            action=self._action,
        )
        self._apply_family(family)

    @property
    def family(self) -> DeviceFamily:
        return self._family

    def set_device_family(self, family: DeviceFamily) -> None:
        """Apply family-specific channels, output range and notes."""
        self._family = family
        self.device.set_choices(self._choices_by_family[family])
        self._apply_family(family)
        update_if_mounted(self)

    def set_data_file(self, path: str) -> None:
        self.data_file.set_value(path)

    def read_request(self) -> SendRequest:
        """Return the form as a request; raises ``ValueError`` with a user message."""
        uses_range = self._family is DeviceFamily.NIDAQ
        return build_send_request(
            self._family,
            self.device.device_label,
            format_channels(self.device.ao_channels),
            self.data_file.value,
            self.timing.sample_period.value,
            self.plot_mode.value,
            self.output_range.value if uses_range else None,
        )

    def set_running(self, running: bool) -> None:
        """Show the send or stop action without notifying the host."""
        self._action.set_running(running)

    def _apply_family(self, family: DeviceFamily) -> None:
        # Arduino pins are digital, so only NI-DAQ exposes an output range.
        self.output_range.visible = family is DeviceFamily.NIDAQ
        self._output_note_text.value = _OUTPUT_NOTES[family]

    def _show_plot_warning(self, mode: str) -> None:
        self._plot_warning.visible = mode == REAL_TIME_PLOT
        update_if_mounted(self._plot_warning)


def _group(*controls: ft.Control) -> ft.Column:
    """Keep a field and its note closer than the gap between form rows."""
    return ft.Column(
        controls=list(controls),
        spacing=FORM_GAP // 2,
        horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
    )
