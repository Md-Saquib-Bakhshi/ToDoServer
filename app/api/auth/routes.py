from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api.auth.services import register_user, authenticate_user, hash_password
from app.api.auth.schemas import SignupRequest, LoginRequest, UpdateUserProfile, UserProfile
from app.database.db import get_db
from app.api.auth.models import User
from app.core.security import get_current_user

router = APIRouter()

# ------------------ Auth Endpoints ------------------ #

@router.post("/signup")
def signup(request: SignupRequest, db: Session = Depends(get_db)):
    return register_user(request.email, request.password, db)

@router.post("/login")
def login(request: LoginRequest, db: Session = Depends(get_db)):
    return authenticate_user(request.email, request.password, db)

# ------------------ Profile Endpoints ------------------ #

# ----------------------------
# Get current user profile
@router.get("/profile", response_model=UserProfile)
def get_profile(current_user: User = Depends(get_current_user)):
    return current_user

# ----------------------------
# Update profile (e.g. email)
@router.put("/profile", response_model=UserProfile)
def update_profile(
    updated: UpdateUserProfile,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    user = db.query(User).filter(User.id == current_user.id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.email = updated.email
    db.commit()
    db.refresh(user)
    return user

# ----------------------------
# Delete user account
@router.delete("/profile")
def delete_profile(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    user = db.query(User).filter(User.id == current_user.id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    db.delete(user)
    db.commit()
    return {"detail": "User deleted successfully"}
