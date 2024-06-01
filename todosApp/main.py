from fastapi import FastAPI
from database import engine
import models
import routers.auth as auth
import routers.todos as todos

app = FastAPI()

models.Base.metadata.create_all(bind = engine)

app.include_router(auth.router)
app.include_router(todos.router)