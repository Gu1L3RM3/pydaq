"""Live signal card for acquisition sessions."""

from __future__ import annotations

from collections.abc import Sequence

from components.charts.axes import format_sample_rate
from components.charts.signal_card import SignalCard
from components.charts.signal_plot import SignalPlot
from components.charts.status_badge import RateIndicator, SessionStatus, StatusBadge
from pydaq.core.acquisition import AcquisitionConfig, SampleBatch


class LiveSignalChart(SignalCard):
    """Live signal card that plots ``SampleBatch`` streams per channel.

    Call ``reset(config)`` before a session and ``append_batch`` per batch.
    """

    def __init__(
        self,
        channels: Sequence[str] = ("A0", "A1"),
        duration_s: float = 100.0,
        sample_period_s: float = 0.01,
    ) -> None:
        self.plot = SignalPlot(channels, duration_s=duration_s)
        self.status = StatusBadge()
        self._rate = RateIndicator(format_sample_rate(sample_period_s))
        super().__init__(
            "Live signal",
            "Real-time data from analog input channels.",
            plot=self.plot,
            indicators=(self.status, self._rate),
        )
        self.plot.show_sample()

    def preview(self, config: AcquisitionConfig) -> None:
        """Fit the chart to ``config`` and redraw the static placeholder curves."""
        self.reset(config)
        self.plot.show_sample()

    def reset(self, config: AcquisitionConfig) -> None:
        """Clear plotted data and fit axes, legend and rate to a new session."""
        self.plot.set_time_range(config.duration_s)
        self.plot.set_series(config.channels)
        self._rate.set_text(format_sample_rate(config.sample_period_s))
        self.status.set_status(SessionStatus.IDLE)

    def append_batch(self, batch: SampleBatch) -> None:
        """Extend each channel line; channels missing from ``reset`` are ignored."""
        self.plot.append(batch.times_s, batch.channel_values)

    def set_acquiring(self, running: bool) -> None:
        """Update status when acquisition starts or stops; an error stays visible."""
        if running:
            self.status.set_status(SessionStatus.RUNNING)
            return
        if self.status.status is not SessionStatus.ERROR:
            self.status.set_status(SessionStatus.IDLE)

    def show_error(self) -> None:
        """Mark the session as failed until the next ``reset``."""
        self.status.set_status(SessionStatus.ERROR)
