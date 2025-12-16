from datetime import datetime, date
from typing import Optional

from pydantic import BaseModel, EmailStr
from .models import Roles, PropertyType, Status


class UserSchema(BaseModel):
    id:int
    username: str
    email: str
    phone_number:Optional[str]
    role: Roles
    avatar: str

class UserCreateSchema(BaseModel):
    username: str
    email: EmailStr
    password: str
    phone_number:Optional[str]
    avatar: str

class UserLoginSchema(BaseModel):
    username: str
    password: str


class CityInSchema(BaseModel):
    name:str

class CityOutSchema(BaseModel):
    id:int
    name:str


class PropertyInSchema(BaseModel):
    house_name:str
    description: str
    price:int
    address:str
    property_type:PropertyType
    max_guests:int
    bedrooms:int
    bathrooms:int
    is_active:bool
    created_date:date
    registered_date:datetime
    city_id:int
    owner_id: int

class PropertyOutSchema(BaseModel):
    id: int
    house_name:str
    description: str
    price:int
    address:str
    property_type:PropertyType
    max_guests:int
    bedrooms:int
    bathrooms:int
    is_active:bool
    created_date:date
    registered_date:datetime
    city_id:int
    owner_id: int


class PropertyImageInSchema(BaseModel):
    images: str
    property_id: int

class PropertyImageOutSchema(BaseModel):
    id: int
    images: str
    property_id: int

class BookingInSchema(BaseModel):
    id: int
    check_in: datetime
    check_out: datetime
    status: Status
    created_at: datetime
    property_id: int
    user_id: int

class BookingOutSchema(BaseModel):
    id: int
    check_in: datetime
    check_out: datetime
    status: Status
    created_at: datetime
    property_id: int
    user_id: int

class ReviewInSchema(BaseModel):
    comment:str
    rating:int
    created_at: datetime
    property_id: int
    guest_id: int

class ReviewOutSchema(BaseModel):
    id: int
    comment:str
    rating:int
    created_at: datetime
    property_id: int
    guest_id: int
