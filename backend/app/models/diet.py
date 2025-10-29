from __future__ import annotations

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, func
from sqlalchemy.orm import relationship

from app.database import Base
from app.models.meal import Meal
from app.models.user import User


class Diet(Base):
    __tablename__ = 'diets'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    trainer_id = Column(Integer, ForeignKey(User.id.expression))
    client_id = Column(Integer, ForeignKey(User.id.expression))
    created_at = Column(DateTime, server_default=func.now())

    meals = relationship(Meal.__name__, back_populates='diet')
