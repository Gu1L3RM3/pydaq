"""Turn Send Data form text into a validated ``SendRequest``.

The request mirrors what the legacy ``SendData`` widgets collect; the domain
integration that loads the file and drives the outputs comes later.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from pydaq.core.acquisition import DeviceFamily
from services.acquisition_form import parse_channels, parse_device_name, parse_seconds

ValueRange = tuple[float, float]


@dataclass(frozen=True)
class SendRequest:
    """Everything needed to replay a data file on output channels.

    ``output_range`` is ``None`` for Arduino, whose outputs are digital.
    """

    device_family: DeviceFamily
    device: str
    channels: tuple[str, ...]
    data_path: Path
    sample_period_s: float
    plot_mode: str
    output_range: ValueRange | None = None


def parse_data_path(text: str) -> Path:
    stripped = text.strip()
    if not stripped:
        raise ValueError("Choose the data file to send.")
    return Path(stripped).expanduser()


def parse_volts(field_name: str, text: str) -> float:
    try:
        return float(text.replace(",", "."))
    except ValueError:
        raise ValueError(f"{field_name} must be a voltage, not {text!r}.") from None


def parse_output_range(minimum_text: str, maximum_text: str) -> ValueRange:
    """Parse the NI-DAQ output range; messages are shown to the user."""
    minimum = parse_volts("Output minimum", minimum_text)
    maximum = parse_volts("Output maximum", maximum_text)
    if minimum >= maximum:
        raise ValueError(
            f"Output minimum ({minimum:g} V) must be below the maximum ({maximum:g} V)."
        )
    return (minimum, maximum)


def build_send_request(
    family: DeviceFamily,
    device_label: str,
    channels_label: str,
    data_path_text: str,
    sample_period_text: str,
    plot_mode: str,
    output_range_text: tuple[str, str] | None = None,
) -> SendRequest:
    output_range = (
        parse_output_range(*output_range_text) if output_range_text is not None else None
    )
    channels = parse_channels(channels_label)
    if not channels:
        raise ValueError("Select at least one output channel.")
    return SendRequest(
        device_family=family,
        device=parse_device_name(device_label),
        channels=channels,
        data_path=parse_data_path(data_path_text),
        sample_period_s=parse_seconds("Sample period", sample_period_text),
        plot_mode=plot_mode,
        output_range=output_range,
    )
