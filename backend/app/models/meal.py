from sqlalchemy import Column, Integer, String, ForeignKey, Float
from sqlalchemy.orm import relationship
from app.database import Base

class Meal(Base):
    __tablename__ = "meals"

    id = Column(Integer, primary_key=True, index=True)
    diet_id = Column(Integer, ForeignKey("diets.id"))
    name = Column(String, nullable=False)  # Ej: Desayuno
    total_calories = Column(Float, default=0)

    foods = relationship("Food", back_populates="meal")
    diet = relationship("Diet", back_populates="meals")
