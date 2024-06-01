from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from routers.userModel import AuthUserModel, bcrypt_context
from database import SessionLocal
from sqlalchemy.orm import Session
from models import users
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import datetime, timedelta
from jose import jwt,JWTError

router = APIRouter()



def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_conn = Annotated[Session, Depends(get_db)]
o_Auth_2 = OAuth2PasswordBearer(tokenUrl='login')

async def authorize(token : Annotated[str, Depends(o_Auth_2)]):
    try:
        payload = jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        
        if payload['sub'] is None or payload['id'] is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Could not validate the credentials'
            )
        
        return {
            "username":payload['sub'],
            "userId":payload['id']
        }
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,                          
                            detail='Could not validate credentials')

user_dependency = Annotated[dict,Depends(authorize)]

@router.get('/get-data')
async def get_data(user : user_dependency):
    return {'msg':'hello {}'.format(user['userId'])}

@router.post('/register')
async def create_user(db:db_conn,user_data : AuthUserModel):
    user = users(username = user_data.username,hashed_password = user_data.password)

    if user is not None:
        db.add(user)
        db.commit()
        db.refresh(user)

        return user
    
    return {'status':'failed'}

SECRET_KEY = 'dsfshfkjsdhfkjewaufhaefiuwalkj23'
ALGORITHM = 'HS256'

def get_user(username:str,password:str,db):
    user = db.query(users).filter(users.username == username).first()
    if user is not None:
        if bcrypt_context.verify(password,user.hashed_password):
            return user
    return False

def create_token(username:str,userId:int,expiry_delta:timedelta):
    try:
        encode = {
            'sub':username,
            'id':userId
        }
        expire = datetime.now() + expiry_delta
        encode['exp'] = expire
        token = jwt.encode(encode,SECRET_KEY,algorithm=ALGORITHM)
        return token
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='could not validate credentials')
    


@router.post('/login')
async def login_user(form_data : Annotated[OAuth2PasswordRequestForm,Depends()],db:db_conn):
    user = get_user(username=form_data.username,password=form_data.password,db=db)
    if user is False:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='user could not be validated')
    token = create_token(username=form_data.username,userId=user.id,expiry_delta=timedelta(minutes=30))
    return token