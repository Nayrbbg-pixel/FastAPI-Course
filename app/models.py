from sqlalchemy import Column, Integer, String
from database import Base

class users(Base):

    __tablename__ = 'users'
    id = Column(Integer,primary_key=True,index=True)
    username = Column(String(150),unique=True)
    hashed_password = Column(String)