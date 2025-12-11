from fastapi import APIRouter, Depends, HTTPException
from booking_app_fastapi.database.models import User
from booking_app_fastapi.database.schema import UserSchema
from booking_app_fastapi.database.db import SessionLocal
from sqlalchemy.orm import Session
from typing import List


user_router = APIRouter(prefix="/users", tags=["Users"])

async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@user_router.get("/")
async def list_user(db: Session = Depends(get_db),response_model=List[UserSchema]):
    user_db = db.query(User).all()
    if user_db is None:
        raise HTTPException(status_code=404, detail="No user found")
    return user_db

@user_router.get('/{user_id}')
async def user_detail(user_id:int, db: Session = Depends(get_db), response_model=UserSchema):
    user_db = db.query(User).filter(User.id == user_id).first()
    if user_db is None:
        raise HTTPException(status_code=404, detail="No user found")
    return user_db
