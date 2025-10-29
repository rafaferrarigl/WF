from __future__ import annotations

from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session, joinedload

from app.database import SessionLocal
from app.models.diet import Diet
from app.models.meal import Meal
from app.models.user import User
from app.routers.auth import get_current_user


router = APIRouter(
    prefix='/diets',
    tags=['diets'],
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


class FoodResponse(BaseModel):
    id: int
    name: str
    grams: float
    protein: float
    carbs: float
    fats: float

    class Config:
        orm_mode = True


class MealResponse(BaseModel):
    id: int
    name: str
    total_calories: float
    foods: list[FoodResponse] = []

    class Config:
        orm_mode = True


class DietResponse(BaseModel):
    id: int
    name: str
    trainer_id: int
    client_id: int
    created_at: datetime
    meals: list[MealResponse] = []

    class Config:
        orm_mode = True


class DietCreate(BaseModel):
    name: str
    client_id: int
    meal_ids: list[int] = []  # IDs de comidas existentes


# ---------------------- 👨‍🏫 Crear dieta (solo entrenadores) ----------------------
@router.post('/', response_model=DietResponse, status_code=status.HTTP_201_CREATED)
async def create_diet(
    diet_request: DietCreate,
    db: db_dependency,
    current_user=Depends(get_current_user),
):
    # Solo entrenadores
    if not current_user['is_admin']:
        raise HTTPException(status_code=403, detail='Solo entrenadores pueden crear dietas.')

    # Verificar que el cliente exista
    client = db.query(User).filter(User.id == diet_request.client_id).first()
    if not client:
        raise HTTPException(status_code=404, detail='Cliente no encontrado.')

    new_diet = Diet(
        name=diet_request.name,
        trainer_id=current_user['id'],
        client_id=diet_request.client_id,
        created_at=datetime.utcnow(),
    )

    db.add(new_diet)
    db.commit()
    db.refresh(new_diet)

    # Asociar comidas existentes por ID
    for meal_id in diet_request.meal_ids:
        meal = db.query(Meal).filter(Meal.id == meal_id).first()
        if not meal:
            raise HTTPException(status_code=404, detail=f'Comida {meal_id} no encontrada.')
        meal.diet_id = new_diet.id
        db.add(meal)
    db.commit()

    return new_diet


# ---------------------- 👀 Ver todas las dietas ----------------------
@router.get('/', response_model=list[DietResponse])
async def get_all_diets(
    db: db_dependency,
    current_user=Depends(get_current_user),
):
    if current_user['is_admin']:
        diets = (
            db.query(Diet)
            .options(joinedload(Diet.meals).joinedload(Meal.foods))
            .filter(Diet.trainer_id == current_user['id'])
            .all()
        )
    else:
        diets = (
            db.query(Diet)
            .options(joinedload(Diet.meals).joinedload(Meal.foods))
            .filter(Diet.client_id == current_user['id'])
            .all()
        )

    return diets


# ---------------------- 🔎 Ver una dieta específica ----------------------
@router.get('/{diet_id}', response_model=DietResponse)
async def get_diet(
    diet_id: int,
    db: db_dependency,
    current_user=Depends(get_current_user),
):
    diet = db.query(Diet).options(joinedload(Diet.meals).joinedload(Meal.foods)).filter(Diet.id == diet_id).first()
    if not diet:
        raise HTTPException(status_code=404, detail='Dieta no encontrada.')

    # Solo el entrenador o el cliente asignado pueden verla
    if not (
        (current_user['is_admin'] and diet.trainer_id == current_user['id'])
        or (not current_user['is_admin'] and diet.client_id == current_user['id'])
    ):
        raise HTTPException(status_code=403, detail='No tienes permiso para ver esta dieta.')

    return diet
