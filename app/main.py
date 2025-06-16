
from fastapi import FastAPI
from app.core.config import settings
from app.api.routes import auth
from app.api.routes import user

app = FastAPI()

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(user.router, prefix="/api", tags=["user"])
