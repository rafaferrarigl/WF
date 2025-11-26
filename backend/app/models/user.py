from __future__ import annotations

from sqlalchemy import Boolean, Column, Date, Float, Integer, String

from app.database import Database


class User(Database.base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)

    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)

    is_admin = Column(Boolean, default=False)

    birth_date = Column(Date, nullable=True)
    height = Column(Float, nullable=True)
    weight = Column(Float, nullable=True)
    gender = Column(String, nullable=True)
