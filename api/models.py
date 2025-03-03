from sqlalchemy import Column, Integer, String, Boolean
from api.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)
    role = Column(String, default="user")
    locked = Column(Boolean, default=False)


class SecurityLog(Base):
    __tablename__ = "security_logs"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(String)
    username = Column(String)
    action = Column(String)
    status = Column(String)
    ip_address = Column(String)
