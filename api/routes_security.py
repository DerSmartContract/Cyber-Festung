from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from api.database import SessionLocal
from api.models import SecurityLog
from api.schemas import SecurityLogSchema
import time

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/logs")
def get_logs(db: Session = Depends(get_db), limit: int = 10):
    """Holt die letzten Security-Logs"""
    logs = db.query(SecurityLog).order_by(SecurityLog.id.desc()).limit(limit).all()
    return logs


@router.post("/log")
def create_log(log_entry: SecurityLogSchema, db: Session = Depends(get_db)):
    """Erstellt einen neuen Security-Log-Eintrag"""
    new_log = SecurityLog(
        timestamp=time.strftime("%Y-%m-%dT%H:%M:%S"),
        username=log_entry.username,
        action=log_entry.action,
        status=log_entry.status,
        ip_address=log_entry.ip_address,
    )
    db.add(new_log)
    db.commit()
    return {"message": "✅ Security-Log gespeichert!", "log": new_log}


@router.get("/threat-detection/{ip}")
def check_threat(ip: str):
    """Simulierte Bedrohungserkennung für eine IP-Adresse"""
    blacklisted_ips = ["192.168.1.100", "203.0.113.50", "45.33.32.156"]
    if ip in blacklisted_ips:
        return {
            "threat_detected": True,
            "ip": ip,
            "message": "⚠️ Verdächtige IP-Adresse erkannt!",
        }
    return {
        "threat_detected": False,
        "ip": ip,
        "message": "✅ Keine Bedrohung erkannt.",
    }
