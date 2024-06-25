from .routers import auth, admin, Users, todos
from .models import Base
from .database import engine
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles 

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_methods = ['*'],
    allow_headers = ['*'],
    allow_credentials = ['*'] 
)

app.mount("/todosApp/static",StaticFiles(directory='todosApp/static'),name='static')

Base.metadata.create_all(bind = engine)

app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(admin.router)
app.include_router(Users.router)