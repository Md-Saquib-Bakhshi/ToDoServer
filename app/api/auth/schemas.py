from typing import Optional
from pydantic import BaseModel, EmailStr

class SignupRequest(BaseModel):
    email: EmailStr
    password: str

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

# What is returned in profile
class UserProfile(BaseModel):
    id: int
    email: EmailStr
    password: Optional[str] = None

    class Config:
        orm_mode = True

# For updating user profile (e.g., only email)
class UpdateUserProfile(BaseModel):
    email: EmailStr
    password: Optional[str] = None
