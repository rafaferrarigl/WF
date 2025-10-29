from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel

from app.database import db_dependency  # noqa: TC001
from app.models.meal import Meal
from app.routers.auth import get_current_user


router = APIRouter(prefix='/meals', tags=['diets'])


# ---------------------- 📦 Esquemas Pydantic ----------------------
class MealCreate(BaseModel):
    name: str
    description: str | None = None
    total_calories: float | None = 0


class FoodResponse(BaseModel):
    id: int
    name: str
    grams: float
    protein: float
    carbs: float
    fats: float


class MealResponse(BaseModel):
    id: int
    name: str
    description: str | None = None
    total_calories: float
    foods: list[FoodResponse] = []


# ---------------------- 👨‍🏫 Crear comida (solo entrenadores) ----------------------
@router.post('/', response_model=MealResponse, status_code=status.HTTP_201_CREATED)
async def create_meal(
    meal: MealCreate,
    db: db_dependency,
    current_user=Depends(get_current_user),
):
    if not current_user['is_admin']:
        raise HTTPException(status_code=403, detail='Solo entrenadores pueden crear comidas.')

    new_meal = Meal(
        name=meal.name,
        description=meal.description,
        total_calories=meal.total_calories,
    )
    db.add(new_meal)
    db.commit()
    db.refresh(new_meal)
    return new_meal


# ---------------------- 🍴 Ver todas las comidas ----------------------
@router.get('/', response_model=list[MealResponse])
async def get_all_meals(
    db: db_dependency,
    current_user=Depends(get_current_user),
):
    return db.query(Meal).all()


# ---------------------- 🔎 Ver una comida específica ----------------------
@router.get('/{meal_id}', response_model=MealResponse)
async def get_meal(
    meal_id: int,
    db: db_dependency,
    current_user=Depends(get_current_user),
):
    meal = db.query(Meal).filter(Meal.id == meal_id).first()
    if not meal:
        raise HTTPException(status_code=404, detail='Comida no encontrada.')
    return meal
