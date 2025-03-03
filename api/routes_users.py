from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from api.database import SessionLocal
from api.models import User

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/")
def list_users(db: Session = Depends(get_db)):
    """Listet alle User auf (Admin-Only)"""
    users = db.query(User).all()
    return users
