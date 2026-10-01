"""Tests for chart axis and label helpers."""

from __future__ import annotations

import pytest

from components.charts.axes import (
    CHANNEL_COLORS,
    channel_color,
    format_sample_rate,
    time_axis_ticks,
    value_axis_ticks,
)


@pytest.mark.parametrize(
    ("duration_s", "expected"),
    [
        (100, tuple(range(0, 101, 10))),
        (150, tuple(range(0, 141, 20))),
        (7, tuple(range(0, 8))),
        (0.5, (0,)),
    ],
)
def test_time_axis_ticks_use_round_steps(duration_s: float, expected: tuple[int, ...]) -> None:
    assert time_axis_ticks(duration_s) == expected


def test_time_axis_ticks_reject_non_positive_duration() -> None:
    with pytest.raises(ValueError, match="duration_s must be positive, received 0"):
        time_axis_ticks(0)


@pytest.mark.parametrize(
    ("value_range", "expected"),
    [
        ((-6, 6), (-6, -4, -2, 0, 2, 4, 6)),
        ((0, 100), (0, 20, 40, 60, 80, 100)),
        ((0, 1), (0, 0.2, 0.4, 0.6, 0.8, 1)),
        ((-1.5, 2.5), (-1, 0, 1, 2)),
    ],
)
def test_value_axis_ticks_use_round_steps(
    value_range: tuple[float, float], expected: tuple[float, ...]
) -> None:
    assert value_axis_ticks(value_range) == pytest.approx(expected)


def test_value_axis_ticks_reject_empty_range() -> None:
    with pytest.raises(ValueError, match="low < high"):
        value_axis_ticks((5, 5))


def test_format_sample_rate_inverts_period() -> None:
    assert format_sample_rate(0.01) == "100 Hz"
    assert format_sample_rate(0.4) == "2.5 Hz"


def test_channel_color_cycles_through_palette() -> None:
    assert channel_color(0) == CHANNEL_COLORS[0]
    assert channel_color(len(CHANNEL_COLORS)) == CHANNEL_COLORS[0]
