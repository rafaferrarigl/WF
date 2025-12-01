from sqlalchemy import Integer, Column, ForeignKey, Float
from sqlalchemy.orm import relationship

from app.database import Database
from app.models.exercise import Exercise
from app.models.user import User


class ExerciseProgress(Database.base):
    __tablename__ = 'exercise_progress'

    id = Column(Integer, primary_key=True, index=True)
    exercise_id = Column(Integer, ForeignKey(Exercise.id.expression))
    user_id = Column(Integer, ForeignKey(User.id.expression))
    weight = Column(Float, nullable=True)
    repetitions = Column(Integer, nullable=True)

    exercise = relationship('Exercise', back_populates='progress')
