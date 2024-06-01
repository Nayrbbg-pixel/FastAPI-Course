from datetime import datetime, timedelta
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session 
from database import SessionLocal
from models import Users
from routers.userModel import AuthUserModel, Token
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from routers.userModel import bcrypt_context
from jose import JWTError, jwt

router = APIRouter(
    prefix='/auth',
    tags=['authentication']
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_conn = Annotated[Session, Depends(get_db)]

SECRET_KEY = '1a10ab2940f7a4ecdd8dab30a21f6c4e24356b3999cb9143eb380c925980cddf'
ALGORITHM = 'HS256'

oAuth2Pass =  OAuth2PasswordBearer(tokenUrl='auth/login')

def authenticate_user(username : str,password : str, db):
    user = db.query(Users).filter(Users.username == username).first()
    if user is not None:
        if bcrypt_context.verify(password,user.hashed_password):
            return user
        return False
    return False

def create_access_token(username : str, userId : int, expires_delta : timedelta):
    encode = {'sub':username, 'id':userId}
    expires = datetime.now() + expires_delta

    encode['exp'] = expires

    return jwt.encode(encode,SECRET_KEY,algorithm=ALGORITHM)

@router.post('/register',status_code=status.HTTP_201_CREATED)
async def get_user(db : db_conn,user_request:AuthUserModel):
    
    user = Users(
        email = user_request.email,
        username = user_request.username,
        first_name = user_request.first_name,
        last_name = user_request.last_name,
        hashed_password = user_request.password,
        role = user_request.role,
        is_active = True
    )

    if user is not None:
        
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail='Validation Error!')

@router.get('/get-users')
async def get_auth_users(db:db_conn):
    return db.query(Users).all()

async def authorize(token : Annotated[str,Depends(oAuth2Pass)]):
    try:
        payload = jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])

        username : str = payload['sub']
        userId : str = payload['id']

        if username is None or userId is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Could not validate the credentials'
            )
        
        return {'username':username,'id':userId}
    except JWTError:
        raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Could not validate the credentials'
            )

@router.post('/login', response_model=Token)
async def authenticate(db:db_conn,
                       form_data : Annotated[OAuth2PasswordRequestForm,Depends()]):
    user = authenticate_user(form_data.username,form_data.password,db=db)
    if user is not False:

        token = create_access_token(username=form_data.username,
                                   userId = user.id,
                                   expires_delta=timedelta(minutes=20)
                                   )

        return {'access_token':token,'token_type':'bearer'}
    
    raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Could not validate the credentials'
            )

