from pydantic import BaseModel
from uuid import UUID
from typing import Optional


class LoginRequest(BaseModel):
    email: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    user_id: UUID
    email: Optional[str] = None


class UserCreate(BaseModel):
    email: str
    password: str
    first_name: str
    last_name: str


class UserResponse(BaseModel):
    id: UUID
    email: str
    first_name: str
    last_name: str
    is_active: bool
    is_superuser: bool

    model_config = {"from_attributes": True}
