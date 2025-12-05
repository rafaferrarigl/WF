from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

from app.database import Database



class RoutineExercise(Database.base):
    __tablename__ = 'routine_exercise'

    id = Column(Integer, primary_key=True)
    exercise_id = Column(Integer, ForeignKey('exercises.id'), nullable=False)
    routine_id = Column(Integer, ForeignKey('routines.id'), nullable=False)

    min_repeats = Column(Integer)
    max_repeats = Column(Integer)
    set = Column(Integer)

    exercises = relationship("Exercise", back_populates="routine_exercise")
