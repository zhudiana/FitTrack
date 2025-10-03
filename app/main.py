from fastapi import FastAPI
from app.routers import auth, measurement, google_auth
from app.db import models
from app.db.database import engine


app = FastAPI()

models.Base.metadata.create_all(bind=engine)

app.include_router(measurement.router)
app.include_router(auth.router)
app.include_router(google_auth.router)