from __future__ import annotations

from datetime import datetime  # noqa: TC003

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel

from app.database import DBSession  # noqa: TC001
from app.models.exercise import Exercise
from app.models.routine import Routine
from app.models.user import User
from app.routers.auth import AutoAdminUser, AutoUser  # noqa: TC001
from app.routers.exercises import ExerciseResponse  # noqa: TC001


router = APIRouter(
    prefix='/routines',
    tags=['routines'],
)


# ---------------------- 🔧 Dependencia DB ----------------------


# ---------------------- 📦 Esquemas Pydantic ----------------------


class RoutineCreate(BaseModel):
    name: str
    description: str | None = None
    client_id: int
    exercise_ids: list[int] = []


class RoutineResponse(BaseModel):
    id: int
    name: str
    description: str | None
    created_at: datetime
    trainer_id: int
    client_id: int
    exercises: list[ExerciseResponse] = []


# ---------------------- 👨‍🏫 Crear rutina (solo entrenadores) ----------------------
@router.post('/', response_model=RoutineResponse, status_code=status.HTTP_201_CREATED)
async def create_routine(
    routine_request: RoutineCreate,
    db: DBSession,
    current_user: AutoAdminUser,
):
    # ✅ Verificar que el cliente exista
    client = db.query(User).filter(User.id == routine_request.client_id).first()
    if not client:
        raise HTTPException(status_code=404, detail='Cliente no encontrado.')

    # Crear rutina
    new_routine = Routine(
        name=routine_request.name,
        description=routine_request.description,
        trainer_id=current_user.user_id,
        client_id=routine_request.client_id,
    )
    db.add(new_routine)
    db.commit()
    db.refresh(new_routine)

    # Asociar ejercicios por ID
    for ex_id in routine_request.exercise_ids:
        exercise = db.query(Exercise).filter(Exercise.id == ex_id).first()
        if not exercise:
            raise HTTPException(status_code=404, detail=f'Ejercicio {ex_id} no encontrado')
        exercise.routine_id = new_routine.id
        db.add(exercise)
    db.commit()

    return new_routine


# ---------------------- 👀 Ver todas las rutinas ----------------------
@router.get('/', response_model=list[RoutineResponse])
async def get_all_routines(
    db: DBSession,
    current_user: AutoUser,
):
    filter_element = Routine.trainer_id if current_user.is_admin else Routine.client_id
    # 🧠 Entrenadores ven sus rutinas creadas
    query = db.query(Routine).filter(filter_element == current_user.user_id)

    return query.all()
