"""Sample device and channel choices shown until device discovery exists."""

from __future__ import annotations

from components.setup.device_section import ChannelOptions, DeviceChoices
from pydaq.core.acquisition import DeviceFamily

# Analog-input-only choices for Get Data.
ACQUISITION_DEVICE_CHOICES = {
    DeviceFamily.ARDUINO: DeviceChoices(
        devices=("COM3 · Arduino Uno", "COM4 · Arduino Mega"),
        ai_channels=ChannelOptions(("A0", "A1"), selected=("A0", "A1")),
    ),
    DeviceFamily.NIDAQ: DeviceChoices(
        devices=("Dev1 · NI USB-6009", "Dev2 · NI-DAQ"),
        ai_channels=ChannelOptions(("ai0", "ai1"), selected=("ai0", "ai1")),
    ),
}

# Output-only choices for Send Data. Arduino pins are digital (the legacy widget
# intends D2–D13; D0/D1 carry the serial link) and NI-DAQ channels are analog.
OUTPUT_DEVICE_CHOICES = {
    DeviceFamily.ARDUINO: DeviceChoices(
        devices=("COM3 · Arduino Uno", "COM4 · Arduino Mega"),
        ao_channels=ChannelOptions(
            tuple(f"D{pin}" for pin in range(2, 14)), selected=("D2",)
        ),
    ),
    DeviceFamily.NIDAQ: DeviceChoices(
        devices=("Dev1 · NI USB-6009", "Dev2 · NI-DAQ"),
        ao_channels=ChannelOptions(("ao0", "ao1"), selected=("ao0",)),
    ),
}
