from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.models import user as models
from app.schemas.user import UserCreate, UserRead
from app.schemas.token import Token
from app.db import deps
from app.core.security import hash_password, verify_password, create_jwt_token
from app.core.config import settings


router = APIRouter()


@router.post("/register", response_model=UserRead)
def register_user(
    new_user: UserCreate, 
    db: Session = Depends(deps.get_db)
):
    email_exists = db.query(models.User).filter(models.User.email == new_user.email).first()

    if (email_exists):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    db_user = models.User(
        email = new_user.email,
        hashed_password = hash_password(new_user.password),
        full_name = new_user.full_name,
        is_admin = False,
        is_active = True
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user


@router.post("/login", response_model=Token)
def login(
    user_credentials: OAuth2PasswordRequestForm = Depends(), 
    db: Session = Depends(deps.get_db)
):
    user_exists = db.query(models.User).filter(models.User.email == user_credentials.username).first()

    if not user_exists or not verify_password(user_credentials.password, user_exists.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials: Email or password is incorrect"
        )
    

    access_token = create_jwt_token(data={"sub": user_exists.email}, expires_delta=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    return { "access_token": access_token, "token_type": "bearer"}