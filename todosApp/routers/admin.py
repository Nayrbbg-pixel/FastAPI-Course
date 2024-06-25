from ..database import SessionLocal
from sqlalchemy.orm import Session
from typing import Annotated
from fastapi import APIRouter,Depends, HTTPException, status
from ..models import Todos
from .auth import authorize
from .ValidationModels import Role

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_conn = Annotated[Session,Depends(get_db)]
user_dependency = Annotated[dict,Depends(authorize)]

router = APIRouter(
    tags=['admin'],
    prefix='/admin'
)

@router.get('/get-todo')
async def get_todos(user:user_dependency,db:db_conn):
    if user['role'] != Role.ADMIN:
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED,
                            detail='You are not permitted to be here.')
    
    return db.query(Todos).all()

@router.delete('/delete-todo/{todo_id}')
async def delete_todos(user:user_dependency,db:db_conn,
                       todo_id:int):
    if user['role'] != Role.ADMIN:
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED,
                            detail='You are not permitted to be here.')
    
    todo = db.query(Todos).get(todo_id)
    if todo is None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                            detail='Todo not found')
    
    db.delete(todo)
    db.commit()

    return {"Status":"Success"}