from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///./security_logs.db"  # Später: PostgreSQL-Umstellung

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def init_db():
    """Erstellt die Tabellen, falls sie nicht existieren."""
    from sqlalchemy import inspect
    from api.models import User, SecurityLog  # Modelle importieren

    inspector = inspect(engine)
    if "users" not in inspector.get_table_names():
        Base.metadata.create_all(bind=engine)
        print("✅ Datenbank wurde erfolgreich initialisiert!")
