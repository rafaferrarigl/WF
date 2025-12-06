from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

from app.database import Database



class FoodMeal(Database.base):
    __tablename__ = 'food_meal'

    id = Column(Integer, primary_key=True)
    food_id = Column(Integer, ForeignKey('foods.id'), nullable=False)
    meal_id = Column(Integer, ForeignKey('meals.id'), nullable=False)

    servings = Column(Integer, nullable=False)

    food = relationship("Food", back_populates="food_meal")
    meal = relationship("Meal", back_populates="food_meal")

