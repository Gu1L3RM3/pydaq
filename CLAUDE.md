# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

PyDAQ is moving from PySide6 to a modern Flet UI. Put new UI work in
`flet_ui/`; change PySide6 only for explicit legacy compatibility. Do not make a
widget-for-widget PySide6 port.

## Commands

Python 3.10–3.12 (`requires-python = ">=3.10,<3.13"`). Install with `uv sync`
from the repo root. `pytest` is not a locked dependency, so pass `--with pytest`:

```console
uv run --with pytest pytest flet_ui/tests -q                    # Flet UI unit tests (no hardware)
uv run --with pytest pytest flet_ui/tests/test_chart_axes.py::<test_name>
uv run --with pytest pytest pydaq/tests/tests_pydaq.py -q       # core tests; many need serial ports / NI-DAQmx
uv run --with pytest pytest pydaq/tests/test_acquisition.py pydaq/tests/test_import_boundaries.py -q  # no hardware
uv run python main.py                                           # legacy PySide6 GUI
```

Flet commands run from `flet_ui/`:

```console
cd flet_ui && uv run flet run -r main.py          # desktop, hot reload
cd flet_ui && uv run flet devices
cd flet_ui && uv run flet run --android main.py
cd flet_ui && uv run flet build apk .             # output in flet_ui/build/apk/
cd flet_ui && uv run --with flet-charts flet run examples/live_chart_demo.py
cd flet_ui && uv run flet run examples/components_gallery.py   # shared component kit
```

Failures in `pydaq/tests` about missing COM ports or NI devices are
environmental, not logic regressions. Beyond unit tests, exercise each changed
UI flow on desktop (navigation plus loading, empty, and error states); also
test Android for responsive, touch, or asset changes.

## Architecture

Two GUIs share one domain package:

- **Legacy (PySide6)** — everything Qt lives in `pydaq/legacy_qt/`:
  `main.py` → `pydaq/pydaq_global.py` (shim) → `legacy_qt/app.py`
  (`PydaqGui`). Screens are Qt Designer `.ui` files in `legacy_qt/uis/`
  compiled to `ui_*.py` (promoted-widget headers are relative `..guis.*`, so
  `guis/` and `uis/` must stay siblings); behavior lives in
  `legacy_qt/guis/*_widget.py`, one widget per feature × device. Each widget
  reads form fields, instantiates a domain class (e.g. `GetData()`), sets
  attributes, and calls a blocking method such as `get_data_arduino()`. Use
  these widgets as the reference for *which parameters each feature needs*,
  not for layout. `pydaq/pydaq_global.py` and
  `pydaq/guis/pid_control_window_dialog.py` are compatibility shims for docs
  and notebooks; keep them.
- **Domain** — `pydaq/get_data.py`, `send_data.py`, `step_response.py`,
  `get_model.py`, `pid_control.py`, `lqr_control.py`,
  `data_driven_control.py`, all subclassing `pydaq/utils/base.py:Base`. Each
  class has paired `*_arduino` / `*_nidaq` methods. `NIDAQ_AVAILABLE` in
  `utils/base.py` gates NI-DAQ features when drivers are absent. Domain modules
  must import without PySide6 (`pydaq/tests/test_import_boundaries.py`); the
  legacy error dialogs are reached only through the lazy
  `base._show_error_dialog`.
- **Core (UI-agnostic)** — `pydaq/core/acquisition.py` defines
  `AcquisitionConfig`, `SampleBatch`, and the `AcquisitionSource` protocol
  (configuration in, sample batches out, no plotting or threads). Device
  adapters implementing it go in `pydaq/devices/`; only `simulated.py` exists
  so far. Nothing in `core/` or `devices/` may import Qt, Flet, or matplotlib.
- **New (Flet)** — `flet_ui/`, run as a script directory (imports are
  `from theme import …`, `from components… import …`, not package-relative;
  `flet_ui/tests/conftest.py` puts `flet_ui/` on `sys.path` for the same
  reason, so test folders must not have `__init__.py` or they shadow the real
  packages). `pydaq` is importable because `uv sync` installs the project.
  `main.py:ApplicationShell` hosts one page at a time and swaps
  sidebar ↔ compact header at `MOBILE_BREAKPOINT`. Pages register in
  `pages/routes.py:APP_ROUTES` as `AppRoute(title, icon, build)`, where `build`
  is a zero-arg function returning a control; the menu is derived from it
  (`navigation_items()`), so tuple order is the navigation order.
  Reusable controls go in `components/`: `page_header.py` and
  `workflow_layout.py` (header + setup `lg=4` + results `lg=8`) frame a page;
  `forms/` holds fields, choices (`ChoiceTabs`, `ChannelPicker`) and buttons;
  `setup/` composes `DeviceSection`, `TimingSection` and `OutputSection` into a
  `SetupPanel`; `charts/` has `SignalPlot`, `SignalCard` and `StatusBadge`.
  Build new pages by composing these (see `examples/components_gallery.py`),
  using the legacy `.ui` files for the fields each feature needs. Components
  refresh through `mounting.update_if_mounted`, since Flet 1.0 raises on
  `control.page` before mount and session callbacks can arrive after
  navigation. Sample device/channel options live in `pages/demo_devices.py`
  until device discovery exists. Route-level views go in `pages/` (a
  feature that needs several files becomes `pages/<feature>/`), and the bridge
  to `pydaq.core` in `services/` (`acquisition_form.py` parses form text,
  `acquisition_session.py` runs a source on a worker thread with callbacks).
  Assets are referenced relative to `main.py`'s `assets_dir="assets"`.
  Only Get Data is implemented, streaming from `SimulatedSource`; other routes
  use `pages/placeholder.py`.

### Remaining migration blockers in the domain layer

- The domain classes still plot with matplotlib inside acquisition
  (`plt.show(block=True)`, `Base._start_updatable_plot`), run their own worker
  thread + queue, and show Qt error dialogs at runtime.
- Configuration is set via public attributes after construction, and results
  are written to files under `path` rather than returned.
- Next step: extract `GetData._acquisition_worker_arduino/_nidaq` into
  `pydaq/devices/arduino.py` / `nidaq.py` implementing `AcquisitionSource`,
  then have `GetData` delegate to them (needs hardware validation).
- `flet build apk` packages only `flet_ui/`; shipping `pydaq` to Android needs
  PySide6/nidaqmx made optional extras and a `flet_ui/pyproject.toml`.

## Visual source of truth

Build from the design package at
`flet_ui/assets/pydaq_design_package/pydaq_design_package/` (note the doubled
directory): `index.html` is the responsive prototype, `tokens.json` the
colors/type/spacing, and the two SVGs the full screen and component library.
Reuse its assets and preserve its spacing, hierarchy, colors, typography,
icons, and responsive behavior. Tokens ported to Python live in
`flet_ui/theme.py` (`app_theme()`); never repeat visual values — add new tokens
there.

## Code style

- Python 3.10+, four spaces; `snake_case` for functions/modules/values,
  `PascalCase` for Flet controls; `import flet as ft`.
- Functions 4–20 lines where practical, one responsibility each; a clear Flet
  view composition may be longer. Files stay under 500 lines.
- Specific names; avoid `data`, `handler`, and `Manager`.
- Type public functions, callbacks, and boundaries explicitly. No `Any`,
  `Dict`, or untyped functions; use models, protocols, `Mapping`, or concrete
  collections.
- Prefer early returns, at most two nesting levels, and exceptions that state
  the offending value and the expected shape/range.
- Match nearby formatting; avoid unrelated formatting changes.
- Preserve comments on refactors. Comments explain why. Public reusable APIs
  need intent and a usage example when not self-evident. Cite an issue or
  commit for upstream constraints, quirks, and regressions.

## Tests and dependencies

- Test every testable new function and every bug fix. Keep layout wiring thin;
  test pure state, validation, and mapping logic. Use named fakes — not inline
  stubs — for DAQ, serial, filesystem, and other I/O. Tests are F.I.R.S.T.
- Inject dependencies through constructors or parameters, never globals. Put
  third-party and hardware boundaries behind thin project-owned interfaces.
  Add a dependency only when the current stack cannot meet the need.

## Logging and commits

- Use `logging` for diagnostics with stable structured context (acquisition
  ID, device, action), suitable for JSON sinks. Keep Flet user messages plain,
  actionable, and separate from logs.
- Focused imperative Conventional Commits (`feat:`, `fix:`, `docs:`,
  `refactor:`). PRs describe the user-visible result, linked issue,
  validation, and screenshots or a recording for visual changes.
