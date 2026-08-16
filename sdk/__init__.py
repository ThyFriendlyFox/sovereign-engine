"""Sovereign Engine internal SDK — re-exports lab pack + local cores."""

from __future__ import annotations

import sys
from pathlib import Path

_PACK = Path.home() / "OneDrive" / "internal-sdks"
if _PACK.is_dir() and str(_PACK) not in sys.path:
    sys.path.insert(0, str(_PACK))

from itsnotai_internal.engine_sdk import EngineSDK  # noqa: E402
from itsnotai_internal.grid_sdk import GridSDK  # noqa: E402
from itsnotai_internal.billing_sdk import BillingSDK  # noqa: E402

__all__ = ["EngineSDK", "GridSDK", "BillingSDK"]
