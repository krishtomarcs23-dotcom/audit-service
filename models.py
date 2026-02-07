from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from db import Base   # ✅ import the shared Base

class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True)
    event_type = Column(String, nullable=False)
    actor = Column(String, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
