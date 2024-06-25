from pydantic import (BaseModel,
                      Field,
                      EmailStr,
                      model_validator,
                      )
from enum import Enum
from passlib.context import CryptContext
from fastapi import HTTPException, status

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
    phone_number : str = Field(max_length=10, min_length=10)

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

class ChangePassword(BaseModel):

    current_password : str = Field(min_length=8)
    new_password : str = Field(min_length=8)
    confirmed_password : str = Field(min_length=8)

    class Config:
        json_schema_extra = {
            "example":{
                "current_password":"Enter your current password",
                "new_password":"Enter your new password",
                "confirmed_password":"Confirm your new password"
            }
        }

    @model_validator(mode='after')
    def validation(cls, values):
        if values.new_password != values.confirmed_password:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail='new password did not match the confirmed password')
        values.new_password = bcrypt_context.hash(values.new_password)
        values.confirmed_password = bcrypt_context.hash(values.confirmed_password)
        return values
        
class PhoneNumber(BaseModel):
    phone_number : str = Field(max_length=10, min_length=10)
    
    class Config:
        json_schema_extra = {
            "example":{
                "phone_number":"Add or update phone number."
            }
        }