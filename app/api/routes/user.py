
from fastapi import APIRouter, Depends
from app.core.security import get_current_user
from app.schemas.token import TokenData
from app.schemas.user import UserRead
from app.db.deps import get_db

router = APIRouter()


@router.get('/current_user', response_model=TokenData)
def read_current_user(current_user: TokenData = Depends(get_current_user)):
    return current_user
