from datetime import datetime
from uuid import UUID

from app.models import BaseModel


class SpectatorInput(BaseModel):
    session_id: UUID
    account_id: int


class Spectator(BaseModel):
    session_id: UUID
    account_id: int
    created_at: datetime
