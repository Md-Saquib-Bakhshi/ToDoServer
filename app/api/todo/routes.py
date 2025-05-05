from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer
from app.api.auth.models import User
from app.api.todo.recommend import generate_recommendations_dspy
from app.database.db import get_db
from app.api.todo.schemas import TodoCreate, TodoOut
from app.api.todo.services import (
    create_todo_item, get_user_todos, get_single_todo, update_todo_item, delete_todo_item
)
from app.core.security import get_current_user

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

@router.post("/", response_model=TodoOut)
def create_todo(todo: TodoCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return create_todo_item(todo, db, current_user)

@router.get("/", response_model=list[TodoOut])
def get_all_todos(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return get_user_todos(db, current_user)

@router.get("/{todo_id}", response_model=TodoOut)
def get_todo(todo_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return get_single_todo(todo_id, db, current_user)

@router.put("/{todo_id}", response_model=TodoOut)
def update(todo_id: int, updated: TodoCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return update_todo_item(todo_id, updated, db, current_user)

@router.delete("/{todo_id}")
def delete(todo_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return delete_todo_item(todo_id, db, current_user)

@router.post("/rec/recommendation")
async def get_recommendation():
    try:
        result = await generate_recommendations_dspy()
        return result
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}