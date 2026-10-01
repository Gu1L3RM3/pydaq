"""Tests for the acquisition session lifecycle."""

from __future__ import annotations

from collections.abc import Callable

import pytest

from pydaq.core.acquisition import AcquisitionConfig, DeviceFamily, SampleBatch
from services.acquisition_session import AcquisitionSession

CONFIG = AcquisitionConfig(DeviceFamily.ARDUINO, "COM3", ("A0",), 0.1, 1.0)


def batch_at(time_s: float) -> SampleBatch:
    return SampleBatch(times_s=(time_s,), channel_values={"A0": (time_s,)})


class FakeAcquisitionSource:
    """Replays scripted batches; raises ``failure`` once they run out."""

    def __init__(
        self, batches: tuple[SampleBatch, ...], failure: Exception | None = None
    ) -> None:
        self._pending = list(batches)
        self._failure = failure
        self.started_with: AcquisitionConfig | None = None
        self.stopped = False

    def start(self, config: AcquisitionConfig) -> None:
        self.started_with = config

    def read_batch(self) -> SampleBatch | None:
        if self._pending:
            return self._pending.pop(0)
        if self._failure is not None:
            raise self._failure
        return None

    def stop(self) -> None:
        self.stopped = True


class SessionEvents:
    """Collects callback invocations in order."""

    def __init__(self) -> None:
        self.log: list[str] = []
        self.batches: list[SampleBatch] = []

    def on_batch(self, batch: SampleBatch) -> None:
        self.batches.append(batch)
        self.log.append("batch")

    def on_finished(self) -> None:
        self.log.append("finished")

    def on_error(self, message: str) -> None:
        self.log.append(f"error: {message}")


class DeferredThreadStarter:
    """Holds the worker so tests choose when (and whether) it runs."""

    def __init__(self) -> None:
        self.target: Callable[[], None] | None = None

    def __call__(self, target: Callable[[], None]) -> None:
        self.target = target

    def run(self) -> None:
        assert self.target is not None
        self.target()


def make_session(
    source: FakeAcquisitionSource, events: SessionEvents, starter: DeferredThreadStarter
) -> AcquisitionSession:
    return AcquisitionSession(
        source, events.on_batch, events.on_finished, events.on_error, start_thread=starter
    )


def test_session_streams_until_source_is_exhausted() -> None:
    source = FakeAcquisitionSource((batch_at(0.0), batch_at(0.1)))
    events, starter = SessionEvents(), DeferredThreadStarter()
    session = make_session(source, events, starter)

    session.start(CONFIG)
    assert session.running
    starter.run()

    assert source.started_with == CONFIG
    assert events.log == ["batch", "batch", "finished"]
    assert source.stopped
    assert not session.running


def test_stop_ends_stream_before_next_batch() -> None:
    source = FakeAcquisitionSource((batch_at(0.0), batch_at(0.1)))
    events, starter = SessionEvents(), DeferredThreadStarter()
    session = make_session(source, events, starter)
    session.start(CONFIG)
    session.stop()

    starter.run()

    assert events.log == ["finished"]
    assert source.stopped


def test_source_failure_is_reported_then_finished() -> None:
    source = FakeAcquisitionSource((batch_at(0.0),), failure=OSError("port closed"))
    events, starter = SessionEvents(), DeferredThreadStarter()
    session = make_session(source, events, starter)

    session.start(CONFIG)
    starter.run()

    assert events.log == [
        "batch",
        "error: Acquisition on COM3 stopped: port closed",
        "finished",
    ]
    assert source.stopped
    assert not session.running


def test_start_while_running_is_rejected() -> None:
    source = FakeAcquisitionSource(())
    session = make_session(source, SessionEvents(), DeferredThreadStarter())
    session.start(CONFIG)

    with pytest.raises(RuntimeError, match="already running"):
        session.start(CONFIG)
