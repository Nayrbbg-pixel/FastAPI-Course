from ..database import SessionLocal
from ..models import Users
from .auth import authorize
from .ValidationModels import ChangePassword, bcrypt_context 
from .ValidationModels import PhoneNumber
from typing import Annotated
from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session 

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_conn = Annotated[Session, Depends(get_db)]
user_depends = Annotated[dict, Depends(authorize)]

router = APIRouter(
    prefix='/user',
    tags = ['User']
)

@router.get('/profile')
async def get_profile(user:user_depends, db:db_conn):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Credentials could not be validated.')
    return db.query(Users).get(user['id'])

@router.put('/change-password')
async def change_password(user:user_depends,data:ChangePassword,
                          db : db_conn):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Credentials could not be validated.')
    retrieved_user = db.query(Users).get(user['id'])
    if retrieved_user is not None:
        if bcrypt_context.verify(data.current_password,retrieved_user.hashed_password):
            retrieved_user.hashed_password = data.confirmed_password
            db.commit()
            db.refresh(retrieved_user)
            return {'status':'Success'}
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='The current password you entered was wrong.')
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail='No user found!')

@router.put('/update-phone-number')
async def update_phone_number(data : PhoneNumber, db:db_conn, user:user_depends):
    if data.phone_number is not None:
        user = db.query(Users).get(user['id'])
        if user is not None:
            user.phone_number = data.phone_number
            db.commit()
            db.refresh(user)
            return {'status':'Success'}
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='User not found!')
    
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                        detail='Phone number was not provided!')