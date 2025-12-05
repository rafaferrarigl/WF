from __future__ import annotations

from fastapi import APIRouter, status, HTTPException
from pydantic import BaseModel
from app.database import DBSession, Database
from app.models.exercise import Exercise
from app.routers.auth import AutoAdminUser  # noqa: TC001


router = APIRouter(prefix='/exercises', tags=['routines'])


# ----------------------  Esquemas Pydantic ----------------------
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


# ----------------------  Crear ejercicio ----------------------
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
    return ExerciseResponse(
        id=new_exercise.id,
        name=new_exercise.name,
        description=new_exercise.description,
        video_url=new_exercise.video_url,
        comment=new_exercise.comment,
    )


# ---------------------- Ver ejercios ----------------------
@router.get('/{id}', status_code=status.HTTP_200_OK, response_model=ExerciseResponse)
async def get_exercise(
        db: DBSession,
        id: int,
        current_user: AutoAdminUser,  # noqa: ARG001
) -> ExerciseResponse:
    exercise = db.query(Exercise).get(id)
    if not exercise:
        raise HTTPException(status_code=404, detail="Ejercicio no encontrado")
    return exercise