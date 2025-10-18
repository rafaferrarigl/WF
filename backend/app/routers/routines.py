from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Annotated, List
from datetime import datetime

from app.database import SessionLocal
from app.models.routine import Routine
from app.models.user import User
from app.models.exercise import Exercise
from app.routers.exercises import ExerciseResponse
from app.routers.auth import get_current_user  # ✅ solo usamos esta
from pydantic import BaseModel, Field


router = APIRouter(
    prefix="/routines",
    tags=["routines"]
)

# ---------------------- 🔧 Dependencia DB ----------------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

# ---------------------- 📦 Esquemas Pydantic ----------------------


class RoutineCreate(BaseModel):
    name: str = Field(..., example="Rutina de fuerza - Semana 1")
    description: str | None = Field(None, example="Enfocada en tren inferior y fuerza máxima")
    client_id: int = Field(..., example=3)
    exercise_ids: List[int] = []  # <-- Lista de IDs de ejercicios existentes

class RoutineResponse(BaseModel):
    id: int
    name: str
    description: str | None
    created_at: datetime
    trainer_id: int
    client_id: int
    exercises: list[ExerciseResponse] = []  # <-- aquí se listarán los ejercicios asociados

    class Config:
        orm_mode = True




# ---------------------- 👨‍🏫 Crear rutina (solo entrenadores) ----------------------
@router.post("/", response_model=RoutineResponse, status_code=status.HTTP_201_CREATED)
async def create_routine(
    routine_request: RoutineCreate,
    db: db_dependency,
    current_user=Depends(get_current_user)
):
    # 🚫 Solo entrenadores (is_admin=True) pueden crear rutinas
    if not current_user["is_admin"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Solo los entrenadores pueden crear rutinas."
        )

    # ✅ Verificar que el cliente exista
    client = db.query(User).filter(User.id == routine_request.client_id).first()
    if not client:
        raise HTTPException(status_code=404, detail="Cliente no encontrado.")

    # Crear rutina
    new_routine = Routine(
        name=routine_request.name,
        description=routine_request.description,
        trainer_id=current_user["id"],
        client_id=routine_request.client_id
    )
    db.add(new_routine)
    db.commit()
    db.refresh(new_routine)

    # Asociar ejercicios por ID
    for ex_id in routine_request.exercise_ids:
        exercise = db.query(Exercise).filter(Exercise.id == ex_id).first()
        if not exercise:
            raise HTTPException(status_code=404, detail=f"Ejercicio {ex_id} no encontrado")
        exercise.routine_id = new_routine.id
        db.add(exercise)
    db.commit()

    return new_routine


# ---------------------- 👀 Ver todas las rutinas ----------------------
@router.get("/", response_model=List[RoutineResponse])
async def get_all_routines(
    db: db_dependency,
    current_user=Depends(get_current_user)
):
    # 🧠 Entrenadores ven sus rutinas creadas
    if current_user["is_admin"]:
        routines = db.query(Routine).filter(Routine.trainer_id == current_user["id"]).all()
    else:
        # 🏋️ Clientes ven las que se les asignaron
        routines = db.query(Routine).filter(Routine.client_id == current_user["id"]).all()

    return routines


# ---------------------- 🔎 Ver una rutina específica ----------------------
@router.get("/{routine_id}", response_model=RoutineResponse)
async def get_routine(
    routine_id: int,
    db: db_dependency,
    current_user=Depends(get_current_user)
):
    routine = db.query(Routine).filter(Routine.id == routine_id).first()
    if not routine:
        raise HTTPException(status_code=404, detail="Rutina no encontrada.")

    # ⚖️ Permitir acceso solo al entrenador o al cliente asignado
    if not (
        current_user["is_admin"] and routine.trainer_id == current_user["id"]
    ) and not (
        not current_user["is_admin"] and routine.client_id == current_user["id"]
    ):
        raise HTTPException(status_code=403, detail="No tienes permiso para ver esta rutina.")

    return routine
