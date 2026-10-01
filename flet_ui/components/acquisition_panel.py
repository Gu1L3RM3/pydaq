"""Get Data setup panel composed from the shared setup sections."""

from __future__ import annotations

from collections.abc import Callable, Mapping

from components.forms.buttons import PrimaryActionButton
from components.forms.choices import format_channels
from components.setup.device_section import DeviceChoices, DeviceSection
from components.setup.output_section import OutputSection
from components.setup.setup_panel import SetupPanel
from components.setup.timing_section import TimingSection
from pydaq.core.acquisition import AcquisitionConfig, DeviceFamily
from services.acquisition_form import build_acquisition_config

AcquisitionCallback = Callable[[bool], None]


class AcquisitionSetupPanel(SetupPanel):
    """Device settings and primary acquisition action.

    The action button only requests a change through ``on_acquisition_change``;
    the host confirms it with ``set_running`` once the session starts or ends.
    ``choices_by_family`` must offer AI channels for every family.
    """

    def __init__(
        self,
        choices_by_family: Mapping[DeviceFamily, DeviceChoices],
        on_acquisition_change: AcquisitionCallback | None = None,
        family: DeviceFamily = DeviceFamily.ARDUINO,
    ) -> None:
        self._choices_by_family = choices_by_family
        self._family = family
        self.device = DeviceSection(choices_by_family[family])
        self.timing = TimingSection()
        # Filter, plot and save are presentation only until the domain supports them.
        self.output = OutputSection(show_filter=True)
        self._action = PrimaryActionButton(
            "Start acquisition", "Stop acquisition", on_toggle=on_acquisition_change
        )
        super().__init__(
            "Acquisition setup",
            "Configure your device and acquisition parameters.",
            sections=(self.device, self.timing, self.output),
            action=self._action,
        )

    def set_device_family(self, family: DeviceFamily) -> None:
        """Apply family-specific device and channel options."""
        self._family = family
        self.device.set_choices(self._choices_by_family[family])

    def read_config(self) -> AcquisitionConfig:
        """Return the form as a config; raises ``ValueError`` with a user message."""
        duration = self.timing.duration
        return build_acquisition_config(
            self._family,
            self.device.device_label,
            format_channels(self.device.ai_channels),
            self.timing.sample_period.value,
            duration.value if duration else "",
        )

    def set_running(self, running: bool) -> None:
        """Show the start or stop action without notifying the host."""
        self._action.set_running(running)
