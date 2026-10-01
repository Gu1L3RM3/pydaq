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
