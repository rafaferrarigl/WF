from __future__ import annotations

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import relationship

from app.database import Base


class Routine(Base):
    __tablename__ = 'routines'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    trainer_id = Column(Integer, ForeignKey('users.id'))  # el entrenador que la creó
    client_id = Column(Integer, ForeignKey('users.id'))  # el cliente asignado

    exercises = relationship('Exercise', back_populates='routine')
