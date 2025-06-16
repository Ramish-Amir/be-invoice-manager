from pydantic import BaseModel, EmailStr
from typing import Optional



class UserBase(BaseModel):
    email: EmailStr
    full_name: Optional[str] = None


class UserCreate(UserBase):
    password: str


class UserRead(UserBase):
    id: int
    is_active: bool
    is_admin: bool

    class Config:
        orm_mode = True

class UserLogin(BaseModel):
    email: str
    password: str