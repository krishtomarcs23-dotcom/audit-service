from pydantic import BaseModel
from datetime import datetime


class AuditEventCreate(BaseModel):
    event_type: str
    actor: str


class AuditEventResponse(BaseModel):
    id: int
    event_type: str
    actor: str
    timestamp: datetime

    class Config:
        orm_mode = True
