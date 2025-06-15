from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.models import user as models
from app.schemas.user import UserCreate, UserRead
from app.db import deps
from app.core.security import hash_password


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