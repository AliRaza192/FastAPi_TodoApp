from sqlmodel import SQLModel, Field, create_engine, Session, select
from fastapi import FastAPI, Depends
from typing import Optional , Annotated
import os
from  dotenv import load_dotenv

load_dotenv()

class Todo(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    description: str


class TodoCreate(SQLModel):
    name: str
    description: str

class TodoResponse(SQLModel):
    id: int
    name: str
    description: str




connt_str = os.getenv("DATABASE_URL")
engine = create_engine(connt_str)

def get_data():
    with Session(engine) as session:
        yield session


app: FastAPI = FastAPI (
    title="Todo App", description="A simple todo app", version="0.1.0"
)


@app.get("/todo")
def get_todo(session: Annotated[Session, Depends(get_data)]):
    todo = session.exec(select(Todo)).all()
    return todo


# @app.post("/todo/add", response_model=TodoResponse)
# def add_todo(todo: TodoCreate, session: Annotated[Session,Depends(get_data)]):
#     todo_add = Todo.model_validate(todo)
#     session.add(todo_add)
#     session.commit()
#     session.refresh(todo_add)
#     return todo_add


@app.post("/todo/add", response_model=TodoResponse)
def add_todo(todo: TodoCreate, session: Session = Depends(get_data)):
    # Validation and creating todo
    todo_add = Todo(**todo.dict())
    
    # Adding todo to session and committing
    session.add(todo_add)
    session.commit()
    session.refresh(todo_add)
    
    return todo_add



@app.delete("/todo/delete/{id}", response_model=TodoResponse)
def delete_todo(id: int, session: Annotated [Session, Depends(get_data)]):
    todo_delete = session.get(Todo, id)


    session.delete(todo_delete)
    session.commit()
    return todo_delete



@app.put("/todo/update/{id}", response_model=TodoResponse)
def update_todo(id: int, todo: TodoCreate, session: Annotated[Session, Depends(get_data)]):
    todo_update = session.get(Todo, id)
    if not todo_update:
        return{"error": "todo not found"}

    todo_update.name = todo.name
    todo_update.description = todo.description
    session.commit()
    session.refresh(todo_update)
    return todo_update









# from sqlmodel import SQLModel, Field, create_engine, Session, select
# from fastapi import FastAPI, Depends
# from sqlalchemy.orm import sessionmaker  # Import sessionmaker
# from typing import Optional, Annotated
# import os
# from dotenv import load_dotenv

# load_dotenv()

# class Todo(SQLModel, table=True):
#     id: Optional[int] = Field(default=None, primary_key=True)
#     name: str = Field(index=True)
#     description: str


# class TodoCreate(SQLModel):
#     name: str
#     description: str

# class TodoResponse(SQLModel):
#     id: int
#     name: str
#     description: str

# conn_str = os.getenv("DATABASE_URL")
# engine = create_engine(conn_str)

# # Define a sessionmaker
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# def get_data():
#     # Use sessionmaker to create a Session instance
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()

# app: FastAPI = FastAPI (
#     title="Todo App", description="A simple todo app", version="0.1.0"
# )


# @app.get("/todo")
# def get_todo(session: Annotated[Session, Depends(get_data)]):
#     todo = session.exec(select(Todo)).all()
#     return todo


# @app.get("/todo/add", response_model=TodoResponse)
# def add_todo(todo: TodoCreate, session: Annotated[Session,Depends(get_data)]):
#     todo_add = Todo.model_validate(todo)
#     session.add(todo_add)
#     session.commit()
#     session.refresh(todo_add)
#     return todo_add
