from __future__ import annotations

from fastapi import APIRouter

from . import accounts
from . import sessions
from . import statistics


router = APIRouter()

router.include_router(accounts.router, tags=["accounts"])
router.include_router(sessions.router, tags=["sessions"])
router.include_router(statistics.router, tags=["statistics"])
