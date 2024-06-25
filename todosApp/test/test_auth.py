from datetime import timedelta

from fastapi import HTTPException
from .utils import *
from ..main import app
import pytest
from ..routers.auth import (get_db,
                            authenticate_user,
                            create_access_token,
                            jwt,
                            SECRET_KEY,
                            ALGORITHM,
                            authorize)

app.dependency_overrides[get_db] = overrides_get_db

def test_user_authentication(test_user):
    db = TestingSessionLocal()
    user = authenticate_user('Aryan Raj','testUser',db=db)
    assert user is not None
    assert user.username == 'Aryan Raj'
    assert user.email == 'zyzwe@gmail.com'
    assert user.first_name == 'Aryan'
    assert user.last_name == 'Raj'
    assert user.role == 'admin'

    non_existant_user = authenticate_user('random_non_existant_user','testUser',db=db)
    assert non_existant_user is False

    wrong_password_user = authenticate_user('Aryan Raj','testUser1',db=db)
    assert wrong_password_user is False

def test_create_access_toke(test_user):
    token = create_access_token(test_user.username,test_user.role,
                        test_user.id,timedelta(minutes=30))
    
    assert token is not None
    decoded_token = jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM],
                               options={'verify_signature':False})
    assert decoded_token['sub'] == 'Aryan Raj'
    assert decoded_token['id'] == 1

@pytest.mark.asyncio
async def test_authorization():
    encode = {'sub':'Aryan Raj','id':1,'role':'admin'}
    token = jwt.encode(encode,SECRET_KEY,algorithm=ALGORITHM)
    payload = await authorize(token)

    assert payload['username'] == 'Aryan Raj'
    assert payload['id'] == 1

@pytest.mark.asyncio
async def test_failed_authorization():
    encode = {'role':'admin'}
    token = jwt.encode(encode,SECRET_KEY,algorithm=ALGORITHM)
   
    with pytest.raises(HTTPException) as e:
        await authorize(token=token)
    
    assert e.value.status_code == 401

    