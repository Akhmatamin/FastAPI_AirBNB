import uvicorn
from fastapi import FastAPI
from booking_app_fastapi.api import users,city,booking,review,property


air_bnb = FastAPI()

air_bnb.include_router(users.user_router)
air_bnb.include_router(city.city_router)
air_bnb.include_router(booking.booking_router)
air_bnb.include_router(review.review_router)
air_bnb.include_router(property.property_router)
air_bnb.include_router(property.property_image_router)

if __name__ == '__main__':
    uvicorn.run(air_bnb, host='127.0.0.1', port=8001)


