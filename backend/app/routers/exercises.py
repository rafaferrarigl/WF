from __future__ import annotations

from typing import TYPE_CHECKING

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel

from app.models.exercise import Exercise
from app.routers.auth import get_current_user


if TYPE_CHECKING:
    from app.database import db_dependency


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

    class Config:
        orm_mode = True


# ---------------------- 🏋️ Crear ejercicio ----------------------
@router.post('/', response_model=ExerciseResponse, status_code=status.HTTP_201_CREATED)
async def create_exercise(
    exercise: ExerciseCreate,
    db: db_dependency,
    current_user=Depends(get_current_user),
):
    if not current_user['is_admin']:
        raise HTTPException(status_code=403, detail='Solo entrenadores pueden crear ejercicios')

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
