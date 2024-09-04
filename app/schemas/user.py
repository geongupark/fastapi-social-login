from pydantic import BaseModel
from typing import Optional

class UserCreate(BaseModel):
    email: str
    password: Optional[str] = None
    full_name: Optional[str] = None

class User(BaseModel):
    id: str
    email: str
    full_name: Optional[str] = None
    profile_image: Optional[str] = None
    is_active: bool
    is_social_login: bool

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str
