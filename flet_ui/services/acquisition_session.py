"""Run an ``AcquisitionSource`` off the UI thread and report through callbacks."""

from __future__ import annotations

import logging
import threading
from collections.abc import Callable

from pydaq.core.acquisition import AcquisitionConfig, AcquisitionSource, SampleBatch

logger = logging.getLogger(__name__)

BatchCallback = Callable[[SampleBatch], None]
FinishedCallback = Callable[[], None]
ErrorCallback = Callable[[str], None]
ThreadStarter = Callable[[Callable[[], None]], None]


def start_daemon_thread(target: Callable[[], None]) -> None:
    threading.Thread(target=target, name="pydaq-acquisition", daemon=True).start()


class AcquisitionSession:
    """Own one acquisition run: start, stream batches, stop, report failure.

    Callbacks run on the worker thread; Flet controls may be updated from it.
    ``on_finished`` always runs last, after a normal end, a stop, or an error.
    """

    def __init__(
        self,
        source: AcquisitionSource,
        on_batch: BatchCallback,
        on_finished: FinishedCallback,
        on_error: ErrorCallback,
        start_thread: ThreadStarter = start_daemon_thread,
    ) -> None:
        self._source = source
        self._on_batch = on_batch
        self._on_finished = on_finished
        self._on_error = on_error
        self._start_thread = start_thread
        self._stop_requested = threading.Event()
        self._running = False

    @property
    def running(self) -> bool:
        return self._running

    def start(self, config: AcquisitionConfig) -> None:
        if self._running:
            raise RuntimeError("acquisition is already running; stop it before starting")
        self._stop_requested.clear()
        self._running = True
        self._start_thread(lambda: self._run(config))

    def stop(self) -> None:
        self._stop_requested.set()

    def _run(self, config: AcquisitionConfig) -> None:
        context = {"device": config.device, "family": config.device_family.value}
        try:
            self._source.start(config)
            self._stream()
        except Exception as error:  # device faults must reach the user, not kill the UI
            logger.exception("acquisition failed", extra={**context, "action": "read"})
            self._on_error(f"Acquisition on {config.device} stopped: {error}")
        finally:
            self._source.stop()
            self._running = False
            self._on_finished()

    def _stream(self) -> None:
        while not self._stop_requested.is_set():
            batch = self._source.read_batch()
            if batch is None:
                return
            self._on_batch(batch)
