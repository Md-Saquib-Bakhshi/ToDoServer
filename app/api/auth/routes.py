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
def update_profile(updated_profile: UpdateUserProfile, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    # Find the current user based on their ID (from get_current_user)
    user = db.query(User).filter(User.id == current_user.id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Check if the new email is already taken (other than the current user's own email)
    if updated_profile.email != user.email:
        existing_user = db.query(User).filter(User.email == updated_profile.email).first()
        if existing_user:
            raise HTTPException(status_code=400, detail="Email already registered")

    # Update the user's email and password (if provided)
    user.email = updated_profile.email
    if updated_profile.password:
        user.hashed_password = hash_password(updated_profile.password)  # Hashing new password
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
