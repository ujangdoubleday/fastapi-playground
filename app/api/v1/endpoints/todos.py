from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api import deps
from app.schemas import todo as todo_schemas
from app.models import todo as todo_models

router = APIRouter()

@router.post("/", response_model=todo_schemas.Todo)
def create_todo(todo: todo_schemas.TodoCreate, db: Session = Depends(deps.get_db)):
    db_todo = todo_models.Todo(**todo.model_dump())
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo

@router.get("/", response_model=list[todo_schemas.Todo])
def read_todos(skip: int = 0, limit: int = 100, db: Session = Depends(deps.get_db)):
    todos = db.query(todo_models.Todo).offset(skip).limit(limit).all()
    return todos

@router.get("/{todo_id}", response_model=todo_schemas.Todo)
def read_todo(todo_id: int, db: Session = Depends(deps.get_db)):
    todo = db.query(todo_models.Todo).filter(todo_models.Todo.id == todo_id).first()
    if todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo

@router.put("/{todo_id}", response_model=todo_schemas.Todo)
def update_todo(todo_id: int, todo_in: todo_schemas.TodoUpdate, db: Session = Depends(deps.get_db)):
    db_todo = db.query(todo_models.Todo).filter(todo_models.Todo.id == todo_id).first()
    if db_todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    
    update_data = todo_in.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_todo, key, value)

    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo

@router.delete("/{todo_id}", response_model=todo_schemas.Todo)
def delete_todo(todo_id: int, db: Session = Depends(deps.get_db)):
    db_todo = db.query(todo_models.Todo).filter(todo_models.Todo.id == todo_id).first()
    if db_todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    
    db.delete(db_todo)
    db.commit()
    return db_todo
