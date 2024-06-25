from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from ..database import Base
from sqlalchemy.pool import StaticPool
from ..main import app
from ..models import Todos, Users
import pytest

DATABASE_URL = 'sqlite:///./test.db'
engine = create_engine(
    url=DATABASE_URL,
    connect_args={
        'check_same_thread':False
    },
    poolclass=StaticPool
)

TestingSessionLocal = sessionmaker(bind=engine,
                                   autoflush=False,
                                   autocommit=False)

Base.metadata.create_all(engine)

def overrides_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

def overrides_authorize():
    return {'username':'Aryan Raj','id':1,
            'first_name':'Aryan','last_name':'Raj',
            'is_active':True, 'role':'admin',
            'phone_number':'1234567890'}


@pytest.fixture
def test_todo_cre_del():
    todo = Todos(
        title = 'Test todo',
        description = 'This is a test todo',
        priority = 4,
        complete = False,
        owner_id = 1
    )

    db = TestingSessionLocal()
    db.add(todo)
    db.commit()
    yield todo
    with engine.connect() as connection:
        connection.execute(text('DELETE FROM todos;'))
        connection.commit()


@pytest.fixture
def test_user():
    user = Users(
        username = 'Aryan Raj',
        first_name = 'Aryan',
        last_name = 'Raj',
        email = 'zyzwe@gmail.com',
        hashed_password = '$2b$12$XXu7rlLDSS0m7V/rtE/rI.4J/dFRdme5auOS/egBxictTqcHP32G6',
        phone_number = '1234567890',
        role = 'admin',
        is_active = True,
    )

    db = TestingSessionLocal()
    db.add(user)
    db.commit()
    db.refresh(user)
    yield user

    with engine.connect() as conn:
        conn.execute(text('DELETE FROM users;'))
        conn.commit()