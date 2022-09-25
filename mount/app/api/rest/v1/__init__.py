from __future__ import annotations

from fastapi import APIRouter

from . import accounts
from . import presences
from . import queued_packets
from . import sessions
from . import stats


router = APIRouter()

router.include_router(accounts.router, tags=["accounts"])
router.include_router(presences.router, tags=["presences"])
router.include_router(sessions.router, tags=["sessions"])
router.include_router(stats.router, tags=["stats"])
router.include_router(queued_packets.router, tags=["queued packets"])
