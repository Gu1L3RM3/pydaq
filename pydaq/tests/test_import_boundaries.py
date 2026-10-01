"""Domain modules must import without Qt so non-Qt UIs can use them."""

from __future__ import annotations

import subprocess
import sys

import pytest

DOMAIN_MODULES = (
    "pydaq.core.acquisition",
    "pydaq.devices.simulated",
    "pydaq.utils.base",
    "pydaq.utils.signals",
    "pydaq.get_data",
    "pydaq.send_data",
    "pydaq.step_response",
    "pydaq.get_model",
    "pydaq.pid_control",
    "pydaq.lqr_control",
    "pydaq.data_driven_control",
)


@pytest.mark.parametrize("module", DOMAIN_MODULES)
def test_domain_module_does_not_import_pyside6(module: str) -> None:
    probe = (
        f"import sys, {module}; "
        "loaded = sorted(m for m in sys.modules if m.startswith('PySide6')); "
        "print(','.join(loaded))"
    )
    result = subprocess.run(
        [sys.executable, "-c", probe], capture_output=True, text=True, check=True
    )

    assert result.stdout.strip() == ""


@pytest.mark.parametrize("module", ("pydaq.core.acquisition", "pydaq.devices.simulated"))
def test_core_module_does_not_import_plotting(module: str) -> None:
    probe = f"import sys, {module}; print('matplotlib' in sys.modules)"
    result = subprocess.run(
        [sys.executable, "-c", probe], capture_output=True, text=True, check=True
    )

    assert result.stdout.strip() == "False"
