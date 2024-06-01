from database import Base
from sqlalchemy import (Column,
                        Integer,
                        String,
                        Boolean,
                        ForeignKey
                        )

class Users(Base):

    __tablename__ = 'users'
    id = Column(Integer,primary_key=True,index=True)
    email = Column(String,unique=True)
    username = Column(String(80))
    first_name = Column(String(50))
    last_name = Column(String(40))
    hashed_password = Column(String)
    is_active = Column(Boolean,default=True)
    role = Column(String)

class Todos(Base):
    __tablename__ = 'todos'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(50),nullable=False)
    description = Column(String(150))
    priority = Column(Integer)
    completed = Column(Boolean,default=False)
    owner = Column(Integer,ForeignKey('users.id'))


