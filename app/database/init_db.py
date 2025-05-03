from app.database.db import Base, engine
from app.api.auth.models import User
from app.api.todo.models import Todo

def init_db():
    Base.metadata.create_all(bind=engine)
    print("✅ Tables checked/created.")
