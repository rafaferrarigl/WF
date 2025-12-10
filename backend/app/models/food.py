from sqlalchemy import Column, Float, Integer, String
from sqlalchemy.orm import relationship

from app.database import Database


class Food(Database.base):
    __tablename__ = 'foods'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    serving = Column(String, nullable=False)
    calories = Column(Float, default=0)
    carbs = Column(Float, default=0)
    fats = Column(Float, default=0)
    protein = Column(Float, default=0)
    url = Column(String, nullable=False)

    food_meals = relationship(
        "FoodMeal",
        back_populates="food"
    )
