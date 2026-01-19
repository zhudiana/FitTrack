from fastapi import FastAPI
from app.routers import auth, measurement, google_auth
from app.db import models
from app.db.database import engine
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

models.Base.metadata.create_all(bind=engine)

app.include_router(measurement.router)
app.include_router(auth.router)
app.include_router(google_auth.router)