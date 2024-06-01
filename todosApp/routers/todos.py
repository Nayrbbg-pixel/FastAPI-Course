from fastapi import APIRouter, Depends, HTTPException, Path, status
from pydantic import BaseModel, Field
from database import SessionLocal
from models import Todos
from typing import Annotated, Optional
from sqlalchemy.orm import Session
from routers.auth import authorize
from sqlalchemy import or_, and_

router = APIRouter(
    tags=['todos']
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_conn = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict,Depends(authorize)]

@router.get('/',status_code=status.HTTP_200_OK)
async def home_page(db: db_conn, user : user_dependency):
    return db.query(Todos).filter(Todos.owner == user['id']).all()

@router.get('/todo/{id}',status_code=status.HTTP_200_OK)
async def get_todo(db:db_conn,user : user_dependency,id : int = Path(gt = 0),):
    try:
        todo = db.query(Todos).filter( 
            and_(
            Todos.id == id,
            Todos.owner == user['id']
            )
            ).first()
    except:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='Todo not found!')

    if todo is not None:
        return todo
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail='Todo not found')


class Post(BaseModel):
    title : str = Field(max_length=100)
    description : str = Field(max_length=150)
    priority : int = Field(gt = 0, lt=6)
    completed : bool = Field(default=False)

@router.post('/create-todo',status_code=status.HTTP_201_CREATED)
async def create_todo(db:db_conn,post:Post, user : user_dependency):

    if user['username'] is None or user['id'] is None:

        raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Authentication failed.'
            )
    todo_model = Todos(**post.model_dump(), owner = user['id'])
    db.add(todo_model)
    db.commit()
    db.refresh(todo_model)
    return {'status':'Success!'}

class UpdatePost(BaseModel):
    title : Optional[str] = Field(None,max_length=100)
    description : Optional[str] = Field(None,max_length=150)
    priority : Optional[int] = Field(None,gt = 0, lt=6)
    completed : Optional[bool] = Field(default=None)


@router.put('/update-todo/{todo_id}',status_code=status.HTTP_200_OK)
async def updateTodo(db:db_conn,post:UpdatePost,todo_id:int = Path(gt = 0)):
    
    model = db.query(Todos).get(todo_id)

    if model is not None:
        if post.title is not None:
            model.title = post.title

        if post.description is not None:
            model.description = post.description

        if post.priority is not None:
            model.priority = post.priority

        if post.completed is not None:
            model.completed = post.completed

        db.commit()
        db.refresh(model)  # Refresh to reflect changes
        return model

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail='Todo not found!')


@router.delete('/delete-todo/{todo_id}')
async def delete_todo(db : db_conn,todo_id : int = Path(gt = 0)):
    
    model = db.query(Todos).get(todo_id)

    if model is not None:
        db.delete(model)
        db.commit()

        return {'msg':'Successfully deleted!'}
    
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                         detail='Todo item not found')