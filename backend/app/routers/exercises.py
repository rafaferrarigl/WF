from __future__ import annotations

from fastapi import APIRouter, status
from pydantic import BaseModel
from sqlalchemy import Column, Float, ForeignKey, Integer
from sqlalchemy.orm import relationship

from app.database import Base, db_dependency
from app.models.exercise import Exercise
from app.models.user import User
from app.routers.auth import AutoAdminUser  # noqa: TC001


router = APIRouter(prefix='/exercises', tags=['routines'])


class ExerciseProgress(Base):
    __tablename__ = 'exercise_progress'

    id = Column(Integer, primary_key=True, index=True)
    exercise_id = Column(Integer, ForeignKey(Exercise.id.expression))
    user_id = Column(Integer, ForeignKey(User.id.expression))
    weight = Column(Float, nullable=True)
    repetitions = Column(Integer, nullable=True)

    exercise = relationship('Exercise', back_populates='progress')


# ---------------------- 📦 Esquemas Pydantic ----------------------
class ExerciseCreate(BaseModel):
    name: str
    description: str | None = None
    video_url: str | None = None
    comment: str | None = None


class ExerciseResponse(BaseModel):
    id: int
    name: str
    description: str | None
    video_url: str | None
    comment: str | None


# ---------------------- 🏋️ Crear ejercicio ----------------------
@router.post('/', response_model=ExerciseResponse, status_code=status.HTTP_201_CREATED)
async def create_exercise(
    exercise: ExerciseCreate,
    db: db_dependency,
    current_user: AutoAdminUser,  # noqa: ARG001
):
    new_exercise = Exercise(
        name=exercise.name,
        description=exercise.description,
        video_url=exercise.video_url,
        comment=exercise.comment,
    )
    db.add(new_exercise)
    db.commit()
    db.refresh(new_exercise)
    return new_exercise
