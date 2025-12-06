from __future__ import annotations

from sqlalchemy import Column, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.database import Database
from app.models.meal import Meal


class Food(Database.base):
    __tablename__ = 'foods'

    id = Column(Integer, primary_key=True, index=True)
    meal_id = Column(Integer, ForeignKey(Meal.id.expression))
    name = Column(String, nullable=False)
    calories = Column(Float, default=0)
    carbs = Column(Float, default=0)
    fats = Column(Float, default=0)
    protein = Column(Float, default=0)
    food_url = Column(String, nullable=False)



    meal = relationship('Meal', back_populates='foods')
    food_meals = relationship('FoodMeal', back_populates='foods')