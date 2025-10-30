from typing import Annotated, Literal, Optional
from passlib.context import CryptContext
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.exc import IntegrityError
from pydantic import BaseModel, Field, EmailStr
from app.core.config import ALGORITHM, SECRET_KEY
from app.db.models import Users
from app.dependencies import db_dependency, get_current_user
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt
from datetime import datetime, timedelta, timezone
from app.services.email import send_verification_email
from app.dependencies import user_dependency


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

class PasswordChange(BaseModel):
    current_password: str = Field(min_length=8)
    new_password: str = Field(min_length=8)

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

def create_access_token(data: dict, expires_delta: timedelta):
    encode = data.copy()
    expires = datetime.now(timezone.utc) + expires_delta
    encode.update({"exp": expires})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

@router.post("/token", response_model=Token)
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: db_dependency):
    user = authenticate_user(form_data.username, form_data.password, db)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not getattr(user, "verified_email", False):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Email is not verified",
        )

    token = create_access_token(data={"sub": user.username, "id": user.id}, expires_delta=timedelta(minutes=20))
    return {"access_token": token, "token_type": "Bearer"}



@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(db: db_dependency, create_user_request: CreateUserRequest):
    create_user_model = Users(
        username = create_user_request.username.lower(),
        email=create_user_request.email,
        sex=create_user_request.sex,
        hashed_password=bcrypt_context.hash(create_user_request.password),
        verified_email=False,
    )

    try:
        db.add(create_user_model)
        db.commit()

        await send_verification_email(create_user_request.email, create_user_request.username)

        return {"message": "User created. Please check your email to verify your account."}
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username or email already exists"
        )

@router.get("/verify/{token}")
async def verify_email(token: str, db: db_dependency):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("email")
        if email is None:
            raise HTTPException(status_code=400, detail="Invalid token")

        user = db.query(Users).filter(Users.email == email).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        user.verified_email = True
        db.commit()
        return {"message": "Email verified successfully"}
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=400, detail="Token has expired")
    except jwt.JWTError:
        raise HTTPException(status_code=400, detail="Invalid token")


@router.put("/change_password")
async def change_password(user: user_dependency, db: db_dependency, payload: PasswordChange):
    if not user:
        raise HTTPException(status_code=401, detail="Authentication Failed")

    user_model = db.query(Users).filter(Users.id == user.get('id')).first()

    if not user_model:
        raise HTTPException(status_code=404, detail="User not found")

    if not bcrypt_context.verify(payload.current_password, user_model.hashed_password):
        raise HTTPException(status_code=400, detail="Current password is incorrect")

    if bcrypt_context.verify(payload.new_password, user_model.hashed_password):
        raise HTTPException(status_code=400, detail="New password must be different")

    user_model.hashed_password = bcrypt_context.hash(payload.new_password)

    db.commit()

    return {"message": "Password updated successfully"}