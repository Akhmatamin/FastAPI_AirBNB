from fastapi import APIRouter, Depends, HTTPException
from booking_app_fastapi.database.models import Booking
from booking_app_fastapi.database.schema import BookingInSchema,BookingOutSchema
from booking_app_fastapi.database.db import SessionLocal
from sqlalchemy.orm import Session
from typing import List


booking_router = APIRouter(prefix="/booking", tags=["Booking"])


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@booking_router.get("/", response_model=List[BookingOutSchema])
async def get_booking(db: Session = Depends(get_db)):
    return db.query(Booking).all()

@booking_router.get("/{booking_id}", response_model=BookingOutSchema)
async def detail_booking(booking_id: int, db: Session = Depends(get_db)):
    booking_db = db.query(Booking).filter(Booking.id == booking_id).first()
    if booking_db is None:
        raise HTTPException(status_code=400, detail="Booking not found")
    return booking_db

@booking_router.post("/", response_model=BookingOutSchema)
async def create_booking(booking:BookingInSchema,db:Session = Depends(get_db)):
    booking_db = Booking(**booking.dict())
    db.add(booking_db)
    db.commit()
    db.refresh(booking_db)
    return booking_db

@booking_router.put("/{booking_id}", response_model=BookingOutSchema)
async def update_booking(booking_id: int,booking:BookingInSchema,db:Session = Depends(get_db)):
    booking_db = db.query(Booking).filter(Booking.id == booking_id).first()
    if booking_db is None:
        raise HTTPException(status_code=400, detail="Booking not found")
    for key, value in booking.dict().items():
        setattr(booking_db, key, value)
    db.commit()
    db.refresh(booking_db)
    return booking_db

@booking_router.delete("/{booking_id}", response_model=dict)
async def delete_booking(booking_id: int, db:Session = Depends(get_db)):
    booking_db = db.query(Booking).filter(Booking.id == booking_id).first()
    if booking_db is None:
        raise HTTPException(status_code=400, detail="Booking not found")
    db.delete(booking_db)
    db.commit()
    return {'message': 'Booking deleted'}