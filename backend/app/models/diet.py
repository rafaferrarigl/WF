from __future__ import annotations

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, func
from sqlalchemy.orm import relationship

from app.database import Base


class Diet(Base):
    __tablename__ = 'diets'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    trainer_id = Column(Integer, ForeignKey('users.id'))
    client_id = Column(Integer, ForeignKey('users.id'))
    created_at = Column(DateTime, server_default=func.now())

    meals = relationship('Meal', back_populates='diet')
