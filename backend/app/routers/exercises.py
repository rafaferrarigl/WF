from __future__ import annotations

from fastapi import APIRouter, status
from pydantic import BaseModel
from sqlalchemy import Column, Float, ForeignKey, Integer
from sqlalchemy.orm import relationship

from app.database import DBSession, Database
from app.models.exercise import Exercise
from app.models.user import User
from app.routers.auth import AutoAdminUser  # noqa: TC001


router = APIRouter(prefix='/exercises', tags=['routines'])


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
@router.post('/', status_code=status.HTTP_201_CREATED)
async def create_exercise(
    exercise: ExerciseCreate,
    db: DBSession,
    current_user: AutoAdminUser,  # noqa: ARG001
) -> ExerciseResponse:
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
