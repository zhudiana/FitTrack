from typing import Annotated, Literal, Optional
from passlib.context import CryptContext
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.exc import IntegrityError
from pydantic import BaseModel, Field, EmailStr
from app.core.config import ALGORITHM, SECRET_KEY
from app.db.models import Users
from app.dependencies import db_dependency
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt
from datetime import datetime, timedelta, timezone


router = APIRouter(
    prefix='/auth',
    tags=['auth']
)

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


class CreateUserRequest(BaseModel):
    username: str = Field(min_length=5, max_length=15)
    email: EmailStr     # Validates the right email format
    sex: Optional[Literal["male", "female"]] = None
    password: str = Field(min_length=8)

class Token(BaseModel):
    access_token: str
    token_type: str

def authenticate_user(username: str, password: str, db):
    user = db.query(Users).filter(Users.username == username).first()
    if not user:
        return False
    if not bcrypt_context.verify(password, user.hashed_password):
        return False
    return user 

def create_access_token(username: str, user_id: int, expires_delta: timedelta):
    encode = {"sub": username, "id": user_id}
    expires = datetime.now(timezone.utc) + expires_delta
    encode.update({"exp": expires})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

@router.post("/token", response_model=Token)
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: db_dependency):
    user = authenticate_user(form_data.username, form_data.password, db)

    if not user:
        return "Failed authentication"
    
    token = create_access_token(user.username, user.id, timedelta(minutes=20))
    return {"access_token": token, "token_type": "Bearer"}



@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(db: db_dependency, create_user_request: CreateUserRequest):
    create_user_model = Users(
        username = create_user_request.username,
        email=create_user_request.email,
        sex=create_user_request.sex,
        hashed_password=bcrypt_context.hash(create_user_request.password)
    )

    try:
        db.add(create_user_model)
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username or email already exists"
        )