from fastapi import APIRouter, Depends, HTTPException
from booking_app_fastapi.database.models import Review
from booking_app_fastapi.database.schema import ReviewInSchema,ReviewOutSchema
from booking_app_fastapi.database.db import SessionLocal
from sqlalchemy.orm import Session
from typing import List


review_router = APIRouter(prefix="/review", tags=["Review"])

async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@review_router.get("/",response_model=List[ReviewOutSchema])
async def get_reviews(db: Session = Depends(get_db)):
    return db.query(Review).all()

@review_router.get("/{review_id}",response_model=ReviewOutSchema)
async def detail_review(review_id: int, db:Session = Depends(get_db)):
    review_db = db.query(Review).filter(Review.id==review_id).first()
    if review_db is None:
        raise HTTPException(status_code=400, detail="Review not found")
    return review_db

@review_router.post('/', response_model=dict)
async def create_review(review_data:ReviewInSchema, db:Session = Depends(get_db)):
    review_db = Review(**review_data.dict())
    db.add(review_db)
    db.commit()
    db.refresh(review_db)
    return {'message': 'New review created'}

@review_router.put('/{review_id}',response_model=ReviewOutSchema)
async def update_review(review_id:int, review_data:ReviewInSchema, db:Session = Depends(get_db)):
    review_db = db.query(Review).filter(Review.id == review_id).first()
    if review_db is None:
        raise HTTPException(status_code=400, detail="Review not found")
    for key, value in review_data.dict().items():
        setattr(review_db, key, value)
    db.commit()
    db.refresh(review_db)
    return review_db

@review_router.delete('/{review_id}',response_model=dict)
async def delete_review(review_id:int, db:Session = Depends(get_db)):
    review_db = db.query(Review).filter(Review.id == review_id).first()
    if review_db is None:
        raise HTTPException(status_code=400, detail="Review not found")
    db.delete(review_db)
    db.commit()
    return {'message': 'Review deleted'}