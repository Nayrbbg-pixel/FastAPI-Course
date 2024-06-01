from fastapi import FastAPI
import routers.get as get
import models
from database import engine

app = FastAPI()
app.include_router(get.router)

models.Base.metadata.create_all(bind = engine)