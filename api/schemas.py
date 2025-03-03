from pydantic import BaseModel


class UserCreate(BaseModel):
    username: str
    password: str
    role: str = "user"


class UserLogin(BaseModel):
    username: str
    password: str


class SecurityLogSchema(BaseModel):
    username: str
    action: str
    status: str
    ip_address: str
