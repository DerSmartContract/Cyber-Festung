from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from api.database import SessionLocal
from api.models import User
from api.schemas import UserCreate, UserLogin
import bcrypt

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):
    """Registriert einen neuen Benutzer mit gehashtem Passwort"""
    existing_user = db.query(User).filter(User.username == user.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="❌ User existiert bereits!")

    hashed_pw = bcrypt.hashpw(user.password.encode(), bcrypt.gensalt()).decode()
    new_user = User(username=user.username, password=hashed_pw, role=user.role)

    db.add(new_user)
    db.commit()
    return {"message": "✅ User erfolgreich registriert!"}


@router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    """Validiert den Login eines Benutzers"""
    db_user = db.query(User).filter(User.username == user.username).first()
    if not db_user or not bcrypt.checkpw(
        user.password.encode(), db_user.password.encode()
    ):
        raise HTTPException(
            status_code=401, detail="⛔ Falsches Passwort oder User existiert nicht!"
        )

    return {"message": "✅ Login erfolgreich!"}
