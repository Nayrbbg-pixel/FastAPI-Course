from pydantic import BaseModel, Field, EmailStr, model_validator
from enum import Enum
from passlib.context import CryptContext

bcrypt_context = CryptContext(schemes=['bcrypt'],deprecated = 'auto')

class Role(str,Enum):
    USER = 'user'
    ADMIN = 'admin'

class AuthUserModel(BaseModel):

    email : EmailStr
    first_name : str = Field(max_length= 100,min_length=3)
    last_name : str = Field(max_length= 100,min_length=1)
    username : str = Field(max_length=80)
    password : str = Field(min_length=8)
    role : Role = Field(default=Role.USER)

    class Config:
        json_schema_extra = {
            'example':{
                'email':'Your email',
                'first_name':'Your first_name',
                'last_name':'Your last_name',
                'username':'Your username',
                'password':'Your password',
            }
        }

    @model_validator(mode='after')
    def hash_password(cls,values):
        values.password = bcrypt_context.hash(values.password)
        return values
    

class Token(BaseModel):

    access_token : str
    token_type : str