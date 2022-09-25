from datetime import datetime
from uuid import UUID

from app.models import BaseModel


# input models
class EnqueuePacket(BaseModel):
    data: bytes


# output models
class QueuedPacket(BaseModel):
    session_id: UUID
    data: str
    created_at: datetime
