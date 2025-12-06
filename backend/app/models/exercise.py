from __future__ import annotations

from sqlalchemy import Column, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from app.database import Database
from app.models.routine import Routine


class Exercise(Database.base):
    __tablename__ = 'exercises'

    id = Column(Integer, primary_key=True, index=True)
    routine_id = Column(Integer, ForeignKey('routines.id'))
    name = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    video_url = Column(String, nullable=True)
    comment = Column(Text, nullable=True)

    progress = relationship('ExerciseProgress', back_populates='exercise')

    routine = relationship('Routine', back_populates='exercises')

    routine_exercises = relationship("RoutineExercise", back_populates="exercise")
