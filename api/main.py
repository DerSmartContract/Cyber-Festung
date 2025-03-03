from fastapi import FastAPI
from api.routes_auth import router as auth_router
from api.routes_users import router as users_router
from api.routes_security import router as security_router

app = FastAPI(
    title="Cyber-Festung API",
    description="API zur Verwaltung von Benutzern, Logs & Security-Features",
    version="1.0.0",
)

# Endpoints registrieren
app.include_router(auth_router, prefix="/auth", tags=["Auth"])
app.include_router(users_router, prefix="/users", tags=["Users"])
app.include_router(security_router, prefix="/security", tags=["Security"])


@app.get("/")
def home():
    return {"message": "Welcome to the Cyber-Festung API 🔒"}


# Starte die API mit:
# uvicorn api.main:app --reload
