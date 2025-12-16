from fastapi import APIRouter, HTTPException, Depends
from booking_app_fastapi.database.db import SessionLocal
from booking_app_fastapi.database.models import User, RefreshToken
from booking_app_fastapi.database.schema import UserSchema, UserCreateSchema,UserLoginSchema
from sqlalchemy.orm import Session
from typing import List, Optional
from passlib.context import CryptContext
from jose import jwt
from fastapi.security import OAuth2PasswordBearer
from booking_app_fastapi.config import (SECRET_KEY,ALGORITHMS,ACCESS_TOKEN,REFRESH_TOKEN)
from datetime import datetime,timedelta

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/auth/login')

async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


auth_router = APIRouter(prefix="/auth", tags=["Auth"])

def get_password(password):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] | None = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta if expires_delta else timedelta(minutes=20))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHMS)
    return encoded_jwt

def create_refresh_token(data: dict):
    return create_access_token(data, expires_delta=timedelta(days=10))


@auth_router.post("/register", response_model=dict)
async def register(user_data: UserCreateSchema, db: Session = Depends(get_db)):
    user_db = db.query(User).filter(User.username == user_data.username).first()
    email_db = db.query(User).filter(User.email == user_data.email).first()
    if user_db or email_db:
        raise HTTPException(status_code=400, detail="Username or email already registered")

    hashed_password = get_password(user_data.password)
    user = User(
        username=user_data.username,
        email=user_data.email,
        password=hashed_password,
        phone_number=user_data.phone_number,
        avatar=user_data.avatar,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return {'message': 'User registered'}


@auth_router.post('/login',response_model=dict)
async def login(user_data: UserLoginSchema, db: Session = Depends(get_db)):
    user_db = db.query(User).filter(User.username == user_data.username).first()
    if not user_db or not verify_password(user_data.password, user_db.password):
        raise HTTPException(status_code=401, detail="Username or password are not correct")

    access_token = create_access_token({'sub':user_db.username})
    refresh_token = create_refresh_token({'sub': user_db.username})

    new_token= RefreshToken(
        user_id=user_db.id,
        token=refresh_token,
    )
    db.add(new_token)
    db.commit()

    return {'access_token': access_token, 'refresh_token': refresh_token,'type':'bearer','message': 'Login Successful'}

@auth_router.post('/logout',response_model=dict)
async def logout(refresh_token:str, db: Session = Depends(get_db)):
    stored_token = db.query(RefreshToken).filter(RefreshToken.token==refresh_token).first()
    if stored_token is None:
        raise HTTPException(status_code=401, detail="Refresh Token is invalid")

    db.delete(stored_token)
    db.commit()

    return {'message': 'Logout Successful'}
