
from fastapi import FastAPI
from app.core.config import settings
from app.api.routes import auth

app = FastAPI()

app.include_router(auth.router, prefix="/auth", tags="auth")

@app.get("/")
def read_root():
    return {
        "message": "Fast API starting",
        "db_url": settings.DATABASE_URL,
        "access_token_expiry": settings.ACCESS_TOKEN_EXPIRE_MINUTES
    }