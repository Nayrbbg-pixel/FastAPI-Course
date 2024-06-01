from pydantic import BaseModel, model_validator
from passlib.context import CryptContext 

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated = 'auto')

class AuthUserModel(BaseModel):
    username : str
    password : str

    @model_validator(mode='after')
    def hash_password(cls, vals):
        vals.password = bcrypt_context.hash(vals.password)
        return vals