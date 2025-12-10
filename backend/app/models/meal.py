from __future__ import annotations

from sqlalchemy import Column, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.database import Database
from app.models.diet import Diet


class Meal(Database.base):
    __tablename__ = 'meals'

    id = Column(Integer, primary_key=True, index=True)
    diet_id = Column(Integer, ForeignKey(Diet.id.expression))
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)

    diet = relationship(
        'Diet',
        back_populates='meals'
    )
    food_meals = relationship(
        'FoodMeal',
        back_populates='meal'
    )

