from __future__ import annotations

from sqlalchemy import Column, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.database import Base
from app.models.diet import Diet
from app.models.food import Food


class Meal(Base):
    __tablename__ = 'meals'

    id = Column(Integer, primary_key=True, index=True)
    diet_id = Column(Integer, ForeignKey(Diet.id.expression))
    name = Column(String, nullable=False)  # Ej: Desayuno
    description = Column(String, nullable=True)  # 🆕 Nueva columna
    total_calories = Column(Float, default=0)

    foods = relationship(Food.__name__, back_populates='meal')
    diet = relationship(Diet.__name__, back_populates='meals')
