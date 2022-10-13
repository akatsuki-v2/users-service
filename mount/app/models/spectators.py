from uuid import UUID

from app.models import BaseModel


class SpectatorInput(BaseModel):
    spectator_session_id: UUID
