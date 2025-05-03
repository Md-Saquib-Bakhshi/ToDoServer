from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.api.todo.models import Todo
from app.api.todo.schemas import TodoCreate

def create_todo_item(todo: TodoCreate, db: Session, user):
    new_todo = Todo(**todo.dict(), owner_id=user.id)
    db.add(new_todo)
    db.commit()
    db.refresh(new_todo)
    return new_todo

def get_user_todos(db: Session, user):
    return db.query(Todo).filter(Todo.owner_id == user.id).all()

def get_single_todo(todo_id: int, db: Session, user):
    todo = db.query(Todo).filter(Todo.id == todo_id, Todo.owner_id == user.id).first()
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo

def update_todo_item(todo_id: int, updated_data: TodoCreate, db: Session, user):
    todo = db.query(Todo).filter(Todo.id == todo_id, Todo.owner_id == user.id).first()
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    for key, value in updated_data.dict().items():
        setattr(todo, key, value)
    db.commit()
    db.refresh(todo)
    return todo

def delete_todo_item(todo_id: int, db: Session, user):
    todo = db.query(Todo).filter(Todo.id == todo_id, Todo.owner_id == user.id).first()
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    db.delete(todo)
    db.commit()
    return {"message": "Todo deleted"}
