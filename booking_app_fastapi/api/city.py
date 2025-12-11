from fastapi import APIRouter, Depends, HTTPException
from booking_app_fastapi.database.models import City
from booking_app_fastapi.database.schema import CityInSchema,CityOutSchema
from booking_app_fastapi.database.db import SessionLocal
from sqlalchemy.orm import Session
from typing import List


city_router = APIRouter(prefix="/city", tags=["Cities"])


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@city_router.get("/", response_model=List[CityOutSchema])
async def get_cities(db: Session = Depends(get_db)):
    return db.query(City).all()

@city_router.get('/{city_id}',response_model=CityOutSchema)
async def city_detail(city_id: int, db:Session = Depends(get_db)):
    city_db = db.query(City).filter(City.id==city_id).first()
    if city_db is None:
        raise HTTPException(status_code=400, detail="City not found")
    return city_db

@city_router.post('/',response_model=CityOutSchema)
async def create_city(city:CityInSchema, db: Session = Depends(get_db)):
    city_db = City(**city.dict())
    db.add(city_db)
    db.commit()
    db.refresh(city_db)
    return city_db

@city_router.put("/{city_id}",response_model=dict)
async def update_city(city_id:int,city_data:CityInSchema, db:Session=Depends(get_db)):
    city_db = db.query(City).filter(City.id==city_id).first()
    if city_db is None:
        raise HTTPException(status_code=400, detail="City not found")
    for key,value in city_data.dict().items():
        setattr(city_db,key,value)
    db.commit()
    db.refresh(city_db)
    return {'message':'City updated successfully!'}

@city_router.delete("/{city_id}",response_model=dict)
async def delete_city(city_id:int, db:Session=Depends(get_db)):
    city_db = db.query(City).filter(City.id==city_id).first()
    if city_db is None:
        raise HTTPException(status_code=400, detail="City not found")
    db.delete(city_db)
    db.commit()
    return {'message':'City deleted successfully!'}


