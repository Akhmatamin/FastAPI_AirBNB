from datetime import date,datetime

from .db import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, Enum, Text, ForeignKey, Boolean, Date,DateTime
from typing import Optional, List
from enum import Enum as PyEnum

class Roles(str, PyEnum):
    guest = "guest"
    host = "host"
    admin = "admin"

class PropertyType(str, PyEnum):
    apartment = "apartment"
    studio = "studio"
    house = "house"

class Status(str, PyEnum):
    pending = "pending"
    approved = "approved"
    rejected = "rejected"
    cancelled = "cancelled"

class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(30),unique=True)
    email: Mapped[str] = mapped_column(String(50),unique=True)
    password: Mapped[str] = mapped_column(String,nullable=False)
    phone_number: Mapped[Optional[str]] = mapped_column(String(30),unique=True,nullable=True)
    role: Mapped[Roles] = mapped_column(Enum(Roles), default=Roles.guest)
    avatar: Mapped[Optional[str]] = mapped_column(String, nullable=True)

    user_properties:Mapped[List['Property']] = relationship('Property', back_populates='owner',
                                                            cascade='all, delete-orphan')
    user_bookings: Mapped[List['Booking']] = relationship('Booking', back_populates='guest_booking',
                                                          cascade='all, delete-orphan')
    user_reviews:Mapped[List['Review']] = relationship('Review', back_populates='guest_review',
                                                       cascade='all, delete-orphan')
    user_tokens: Mapped[List['RefreshToken']] = relationship('RefreshToken', back_populates='token_user',
                                                             cascade='all, delete-orphan')


class RefreshToken(Base):
    __tablename__ = 'refresh_tokens'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    token: Mapped[str] = mapped_column(String)

    user_id:Mapped[int] = mapped_column(ForeignKey('users.id'))
    token_user:Mapped[User] = relationship('User', back_populates='user_tokens')
    created_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

class City(Base):
    __tablename__ = 'city'

    id: Mapped[int] = mapped_column(Integer,primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String,nullable=False)

    properties: Mapped[List['Property']] = relationship('Property', back_populates='city',
                                                        cascade="all, delete-orphan")

class Property(Base):
    __tablename__ = 'property'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    house_name: Mapped[str] = mapped_column(String,nullable=False)
    description: Mapped[str] = mapped_column(Text)
    price: Mapped[int] = mapped_column(Integer)
    address:Mapped[str] = mapped_column(String)
    property_type: Mapped[PropertyType] = mapped_column(Enum(PropertyType), default=PropertyType.apartment)
    max_guests:Mapped[str] = mapped_column(Integer)
    bedrooms:Mapped[int] = mapped_column(Integer)
    bathrooms: Mapped[int] = mapped_column(Integer)
    is_active:Mapped[bool] = mapped_column(Boolean)
    # rules
    created_date: Mapped[date] = mapped_column(Date, default=date.today)
    registered_date:Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    city_id: Mapped[int] = mapped_column(ForeignKey('city.id'))
    city: Mapped[City] = relationship(City,back_populates='properties')
    owner_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    owner: Mapped[User] = relationship(User,back_populates='user_properties')
    property_images: Mapped[List['PropertyImage']] = relationship('PropertyImage', back_populates='image_property',
                                                                  cascade='all, delete-orphan')
    property_bookings: Mapped[List['Booking']] = relationship('Booking', back_populates='booking_property',
                                                               cascade='all, delete-orphan')
    property_reviews: Mapped[List['Review']] = relationship('Review', back_populates='reviews',
                                                            cascade='all, delete-orphan')


class PropertyImage(Base):
    __tablename__ = 'property_image'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    images:Mapped[str] = mapped_column(String)

    property_id: Mapped[int] = mapped_column(ForeignKey('property.id'))
    image_property: Mapped[Property] = relationship(Property,back_populates='property_images')


class Booking(Base):
    __tablename__ = 'booking'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    check_in: Mapped[datetime] = mapped_column(DateTime)
    check_out: Mapped[datetime] = mapped_column(DateTime)
    status: Mapped[Status] = mapped_column(Enum(Status))
    created_at:Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    property_id: Mapped[int] = mapped_column(ForeignKey('property.id'))
    booking_property: Mapped[Property] = relationship(Property,back_populates='property_bookings')
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    guest_booking: Mapped[User] = relationship(User,back_populates='user_bookings')


class Review(Base):
    __tablename__ = 'review'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    comment:Mapped[str] = mapped_column(Text,nullable=True)
    rating:Mapped[int] = mapped_column(Integer)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    property_id:Mapped[int] = mapped_column(ForeignKey('property.id'))
    reviews:Mapped[Property] = relationship(Property,back_populates='property_reviews')
    guest_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    guest_review:Mapped[User] = relationship(User,back_populates='user_reviews')
