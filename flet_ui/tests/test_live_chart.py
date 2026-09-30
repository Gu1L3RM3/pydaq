"""Tests for reusable signal chart data preparation."""

from __future__ import annotations

import pytest

from components.live_chart import build_demo_series


def test_build_demo_series_returns_aligned_channels() -> None:
    first, second = build_demo_series(duration=10, point_count=5)

    assert first.name == "A0"
    assert second.name == "A1"
    assert len(first.points) == len(second.points) == 5
    assert first.points[0].time == second.points[0].time == 0
    assert first.points[-1].time == second.points[-1].time == 10


@pytest.mark.parametrize(
    ("duration", "point_count", "message"),
    [
        (0, 5, "duration must be positive"),
        (10, 1, "point_count must be at least 2"),
    ],
)
def test_build_demo_series_rejects_invalid_ranges(
    duration: float,
    point_count: int,
    message: str,
) -> None:
    with pytest.raises(ValueError, match=message):
        build_demo_series(duration=duration, point_count=point_count)
