from pydantic import BaseModel

class TodoCreate(BaseModel):
    title: str
    description: str

class TodoOut(TodoCreate):
    id: int
    completed: bool

    class Config:
        orm_mode = True
