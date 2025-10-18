from sqlalchemy import Column, Integer, String, Boolean, Date, Float
from app.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_admin = Column(Boolean, default=False)

 
    birth_date = Column(Date, nullable=True)  # Fecha de nacimiento
    height = Column(Float, nullable=True)     # Altura en metros
    weight = Column(Float, nullable=True)     # Peso en kg
