from datetime import datetime, timedelta
from jose import JWTError, jwt
from routers.userModel import Token

SECRET_KEY = 'szsx0FgzWDWv2MdXraLwb2kP8sZVOJnaYZ0jg-gsYnM'

def create_access_toke(username:str,userId:int,expires_delta:timedelta) -> Token:

    encode = {
        'sub':username,
        'id':userId
    }

    expires = datetime.now() + expires_delta

    encode['exp'] = expires

    jwt_token = jwt.encode(encode,SECRET_KEY,algorithm='HS256')

    return {'access_token': jwt_token,'token_type':'bearer'}

# print(create_access_toke(username='test',userId=2,expires_delta=timedelta(minutes=30)))


def decode_jwt(token : str):

    try:
        payload = jwt.decode(token,SECRET_KEY,algorithms=['HS256'])
        username : str = payload['sub']
        userId : int = payload['id']
        expiry : timedelta = payload['exp']

        if username is None or userId is None or expiry == datetime.now():
            return 'Could not be authenticated'
        
        return payload
    
    except JWTError as j:
        raise j
    
print(decode_jwt('eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ0ZXN0IiwiaWQiOjIsImV4cCI6MTcxNzIwMzk2Nn0.qS10YeTM693UG17E1r8cfIZLH1gcBsnEwTjHMxscZBI'))