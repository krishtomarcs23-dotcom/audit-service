from fastapi import FastAPI, Depends, Query
from sqlalchemy.orm import Session
import time

from db import SessionLocal, engine
from models import AuditLog
from db import Base

from schemas import AuditEventCreate, AuditEventResponse
from auth import verify_api_key

app = FastAPI(title="Audit Service")


# ---------- Database Dependency ----------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ---------- Startup: wait for DB ----------
@app.on_event("startup")
def on_startup():
    retries = 5
    while retries > 0:
        try:
            
            print("✅ Database connected and tables ready")
            break
        except Exception as e:
            retries -= 1
            print("⏳ Database not ready, retrying...", e)
            time.sleep(2)
    else:
        raise RuntimeError("❌ Database not available after retries")


# ---------- Health Check (public) ----------
@app.get("/health")
def health():
    return {"status": "ok"}


# ---------- Create Audit Event (protected) ----------
@app.post("/events", response_model=AuditEventResponse)
def ingest_event(
    event: AuditEventCreate,
    db: Session = Depends(get_db),
    _: str = Depends(verify_api_key),
):
    audit_event = AuditLog(
        event_type=event.event_type,
        actor=event.actor,
    )

    db.add(audit_event)
    db.commit()
    db.refresh(audit_event)

    return audit_event
# ---------- Get Audit Events (protected + paginated) ----------
@app.get("/events", response_model=list[AuditEventResponse])
def get_events(
    db: Session = Depends(get_db),
    _: str = Depends(verify_api_key),
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0),
    event_type: str | None = None,
    actor: str | None = None,
):
    query = db.query(AuditLog)

    if event_type:
        query = query.filter(AuditLog.event_type == event_type)

    if actor:
        query = query.filter(AuditLog.actor == actor)

    return query.offset(offset).limit(limit).all()
