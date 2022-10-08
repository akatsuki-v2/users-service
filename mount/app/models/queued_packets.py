from datetime import datetime

from app.models import BaseModel


# input models
class EnqueuePacket(BaseModel):
    data: list[int]


# output models
class QueuedPacket(BaseModel):
    data: list[int]
    created_at: datetime
