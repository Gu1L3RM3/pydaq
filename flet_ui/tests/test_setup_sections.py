"""Tests for setup sections and the Get Data panel composition."""

from __future__ import annotations

import pytest

from components.acquisition_panel import AcquisitionSetupPanel
from components.forms.fields import LabeledNumberField
from components.setup.device_section import ChannelOptions, DeviceChoices, DeviceSection
from components.setup.output_section import OutputSection
from components.setup.timing_section import TimingSection
from pages.demo_devices import ACQUISITION_DEVICE_CHOICES
from pydaq.core.acquisition import DeviceFamily

STEP_RESPONSE_CHOICES = DeviceChoices(
    ("COM3 · Arduino Uno",),
    ai_channels=ChannelOptions(("A0", "A1"), ("A0",)),
    ao_channels=ChannelOptions(("D9", "D10"), ("D9",)),
)


def test_device_section_exposes_ai_and_ao_channels() -> None:
    section = DeviceSection(STEP_RESPONSE_CHOICES)

    assert section.device_label == "COM3 · Arduino Uno"
    assert section.ai_channels == ("A0",)
    assert section.ao_channels == ("D9",)


def test_device_section_without_ao_reports_no_channels() -> None:
    section = DeviceSection(ACQUISITION_DEVICE_CHOICES[DeviceFamily.ARDUINO])

    assert section.ao_picker is None
    assert section.ao_channels == ()


def test_device_section_rejects_choices_with_other_pickers() -> None:
    section = DeviceSection(ACQUISITION_DEVICE_CHOICES[DeviceFamily.ARDUINO])

    with pytest.raises(ValueError, match="same AI/AO pickers"):
        section.set_choices(STEP_RESPONSE_CHOICES)


def test_device_choices_require_a_device() -> None:
    with pytest.raises(ValueError, match="at least one device"):
        DeviceChoices(())


def test_timing_section_appends_extra_fields() -> None:
    step_on = LabeledNumberField("Step ON (s)", "5")
    section = TimingSection(duration=None, extra_fields=(step_on,))

    assert section.duration is None
    assert section.controls == [section.sample_period, step_on]


def test_output_section_omits_disabled_rows() -> None:
    section = OutputSection(show_save=False)

    assert section.save is None
    assert section.digital_filter is None
    assert section.controls == [section.plot_mode, section.path]


def test_acquisition_panel_reads_default_config() -> None:
    panel = AcquisitionSetupPanel(ACQUISITION_DEVICE_CHOICES)

    config = panel.read_config()

    assert config.device_family is DeviceFamily.ARDUINO
    assert config.device == "COM3"
    assert config.channels == ("A0", "A1")
    assert config.sample_period_s == 0.01
    assert config.duration_s == 100


def test_acquisition_panel_switches_family_options() -> None:
    panel = AcquisitionSetupPanel(ACQUISITION_DEVICE_CHOICES)

    panel.set_device_family(DeviceFamily.NIDAQ)
    config = panel.read_config()

    assert config.device_family is DeviceFamily.NIDAQ
    assert (config.device, config.channels) == ("Dev1", ("ai0", "ai1"))
