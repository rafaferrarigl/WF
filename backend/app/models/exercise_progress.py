from sqlalchemy import Column, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class ExerciseProgress(Base):
    __tablename__ = "exercise_progress"

    id = Column(Integer, primary_key=True, index=True)
    exercise_id = Column(Integer, ForeignKey("exercises.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    weight = Column(Float, nullable=True)
    repetitions = Column(Integer, nullable=True)

    exercise = relationship("Exercise", back_populates="progress")
