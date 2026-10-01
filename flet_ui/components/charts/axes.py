"""Pure helpers for chart axes, labels and series colors."""

from __future__ import annotations

import math

import flet as ft
import flet_charts as fch

from theme import MUTED, SIGNAL_A0, SIGNAL_A1, TEXT_XSMALL

CHANNEL_COLORS = (SIGNAL_A0, SIGNAL_A1)
_TICK_STEPS = (1, 2, 5, 10, 20, 50, 100, 200, 500, 1000, 2000, 5000)
_MAX_TIME_TICKS = 11
_VALUE_TICK_MANTISSAS = (1, 2, 5)
_MAX_VALUE_INTERVALS = 6

ValueRange = tuple[float, float]


def channel_color(index: int) -> str:
    return CHANNEL_COLORS[index % len(CHANNEL_COLORS)]


def time_axis_ticks(duration_s: float) -> tuple[int, ...]:
    """Round tick positions covering ``duration_s`` with at most 11 labels."""
    if duration_s <= 0:
        raise ValueError(f"duration_s must be positive, received {duration_s}")
    step = next(
        (step for step in _TICK_STEPS if duration_s / step < _MAX_TIME_TICKS),
        _TICK_STEPS[-1],
    )
    return tuple(range(0, int(duration_s) + 1, step))


def value_tick_step(value_range: ValueRange) -> float:
    """Smallest 1/2/5 × 10ⁿ step splitting the range into at most 6 intervals."""
    low, high = value_range
    if high <= low:
        raise ValueError(
            f"value_range must be (low, high) with low < high, received {value_range}"
        )
    span = high - low
    exponent = math.floor(math.log10(span / _MAX_VALUE_INTERVALS))
    for scale in (10**exponent, 10 ** (exponent + 1)):
        for mantissa in _VALUE_TICK_MANTISSAS:
            if span / (mantissa * scale) <= _MAX_VALUE_INTERVALS:
                return mantissa * scale
    raise AssertionError(f"no tick step found for {value_range}")


def value_axis_ticks(value_range: ValueRange) -> tuple[float, ...]:
    """Evenly stepped ticks inside ``value_range``, e.g. (-6, 6) → -6, -4 … 6."""
    step = value_tick_step(value_range)
    low, high = value_range
    first = math.ceil(low / step - 1e-9)
    last = math.floor(high / step + 1e-9)
    return tuple(round(index * step, 10) for index in range(first, last + 1))


def tick_interval(ticks: tuple[float, ...]) -> float:
    return ticks[1] - ticks[0] if len(ticks) > 1 else 1


def format_sample_rate(sample_period_s: float) -> str:
    if sample_period_s <= 0:
        raise ValueError(f"sample_period_s must be positive, received {sample_period_s}")
    return f"{1 / sample_period_s:g} Hz"


def axis_labels(values: tuple[float, ...]) -> list[fch.ChartAxisLabel]:
    return [
        fch.ChartAxisLabel(
            value=value,
            label=ft.Text(f"{value:g}", size=TEXT_XSMALL, color=MUTED),
        )
        for value in values
    ]
