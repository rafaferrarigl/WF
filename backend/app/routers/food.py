from __future__ import annotations

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel

from app.database import DBSession  # noqa: TC001
from app.models.food import Food
from app.models.meal import Meal
from app.routers.auth import AutoAdminUser  # noqa: TC001


router = APIRouter(prefix='/foods', tags=['diets'])


# ---------------------- 📦 Esquemas Pydantic ----------------------
class FoodCreate(BaseModel):
    name: str
    grams: float
    protein: float
    carbs: float
    fats: float


class FoodResponse(BaseModel):
    id: int
    name: str
    grams: float
    protein: float
    carbs: float
    fats: float


# ---------------------- 🧑‍🍳 Agregar alimento a una comida ----------------------
@router.post('/meal/{meal_id}', status_code=status.HTTP_201_CREATED)
async def add_food_to_meal(
    meal_id: int,
    food: FoodCreate,
    db: DBSession,
    current_user: AutoAdminUser,  # noqa: ARG001
) -> FoodResponse:
    # Solo entrenadores pueden agregar alimentos
    meal = db.query(Meal).filter(Meal.id == meal_id).first()
    if not meal:
        raise HTTPException(status_code=404, detail='Comida no encontrada.')

    new_food = Food(
        name=food.name,
        grams=food.grams,
        protein=food.protein,
        carbs=food.carbs,
        fats=food.fats,
        meal_id=meal.id,
    )
    db.add(new_food)
    db.commit()
    db.refresh(new_food)
    return new_food


# ---------------------- 👀 Ver alimentos de una comida ----------------------
@router.get('/meal/{meal_id}')
async def get_foods_by_meal(
    meal_id: int,
    db: DBSession,
    current_user: AutoAdminUser,  # noqa: ARG001
) -> list[FoodResponse]:
    return db.query(Food).filter(Food.meal_id == meal_id).all()
