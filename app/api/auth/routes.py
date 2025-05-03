from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.db import get_db
from app.api.auth.services import register_user, authenticate_user
from app.api.auth.schemas import SignupRequest, LoginRequest

router = APIRouter()

@router.post("/signup")
def signup(request: SignupRequest, db: Session = Depends(get_db)):
    return register_user(request.email, request.password, db)

@router.post("/login")
def login(request: LoginRequest, db: Session = Depends(get_db)):
    return authenticate_user(request.email, request.password, db)
