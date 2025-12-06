from __future__ import annotations

from datetime import datetime

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel

from app.database import DBSession
from app.models.exercise import Exercise
from app.models.routine import Routine
from app.models.routine_exercise import RoutineExercise
from app.models.user import User
from app.routers.auth import AutoAdminUser, AutoUser
from app.routers.exercises import ExerciseResponse


router = APIRouter(
    prefix='/routines',
    tags=['routines'],
)


# ----------------------  Esquemas Pydantic ----------------------

class RoutineExerciseCreate(BaseModel):
    exercise_id: int
    reps_min: int | None = None
    reps_max: int | None = None
    sets: int | None = None


class RoutineCreate(BaseModel):
    name: str
    description: str | None = None
    client_id: int
    exercises: list[RoutineExerciseCreate] = []


class RoutineExerciseResponse(BaseModel):
    id: int
    exercise: ExerciseResponse
    reps_min: int | None
    reps_max: int | None
    sets: int | None

    class Config:
        orm_mode = True


class RoutineResponse(BaseModel):
    id: int
    name: str
    description: str | None
    created_at: datetime
    trainer_id: int
    client_id: int
    exercises: list[RoutineExerciseResponse] = []

    model_config = {"from_attributes": True}


# ----------------------  Crear rutina ----------------------
@router.post('/', status_code=status.HTTP_201_CREATED)
async def create_routine(
    routine_request: RoutineCreate,
    db: DBSession,
    current_user: AutoAdminUser,
) -> RoutineResponse:

    client = db.query(User).filter(User.id == routine_request.client_id).first()
    if not client:
        raise HTTPException(status_code=404, detail='Cliente no encontrado.')

    new_routine = Routine(
        name=routine_request.name,
        description=routine_request.description,
        trainer_id=current_user.user_id,
        client_id=routine_request.client_id,
    )
    db.add(new_routine)
    db.commit()
    db.refresh(new_routine)

    for ex in routine_request.exercises:

        exercise = db.query(Exercise).filter(Exercise.id == ex.exercise_id).first()
        if not exercise:
            raise HTTPException(
                status_code=404,
                detail=f'Ejercicio {ex.exercise_id} no encontrado'
            )

        routine_ex = RoutineExercise(
            routine_id=new_routine.id,
            exercise_id=ex.exercise_id,
            reps_min=ex.reps_min,
            reps_max=ex.reps_max,
            sets=ex.sets,
        )

        db.add(routine_ex)

    db.commit()
    db.refresh(new_routine)

    return new_routine


# ---------------------- Ver rutinas ----------------------
@router.get('/')
async def get_all_routines(
    db: DBSession,
    current_user: AutoUser,
) -> list[RoutineResponse]:
    filter_element = Routine.trainer_id if current_user.is_admin else Routine.client_id

    routines = db.query(Routine).filter(filter_element == current_user.user_id).all()

    return routines
