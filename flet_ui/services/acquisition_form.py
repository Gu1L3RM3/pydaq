"""Turn acquisition form text into a validated ``AcquisitionConfig``."""

from __future__ import annotations

from pydaq.core.acquisition import AcquisitionConfig, DeviceFamily

# Device options read "<port> · <description>", e.g. "COM3 · Arduino Uno".
_DEVICE_LABEL_SEPARATOR = " · "


def parse_device_name(label: str) -> str:
    return label.split(_DEVICE_LABEL_SEPARATOR, 1)[0].strip()


def parse_channels(label: str) -> tuple[str, ...]:
    return tuple(channel.strip() for channel in label.split(",") if channel.strip())


def parse_seconds(field_name: str, text: str) -> float:
    """Parse a positive number of seconds; messages are shown to the user."""
    try:
        seconds = float(text.replace(",", "."))
    except ValueError:
        raise ValueError(f"{field_name} must be a number of seconds, not {text!r}.") from None
    if seconds <= 0:
        raise ValueError(f"{field_name} must be greater than zero, not {text!r}.")
    return seconds


def build_acquisition_config(
    family: DeviceFamily,
    device_label: str,
    channels_label: str,
    sample_period_text: str,
    duration_text: str,
) -> AcquisitionConfig:
    sample_period_s = parse_seconds("Sample period", sample_period_text)
    duration_s = parse_seconds("Session duration", duration_text)
    if duration_s < sample_period_s:
        raise ValueError("Session duration must be at least one sample period.")
    return AcquisitionConfig(
        device_family=family,
        device=parse_device_name(device_label),
        channels=parse_channels(channels_label),
        sample_period_s=sample_period_s,
        duration_s=duration_s,
    )
