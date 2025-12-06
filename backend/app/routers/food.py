from __future__ import annotations

from typing import Any, Coroutine

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel

from app.database import DBSession  # noqa: TC001
from app.models.food import Food
from app.routers.auth import AutoAdminUser  # noqa: TC001


router = APIRouter(prefix='/foods', tags=['diets'])


# ---------------------- Esquemas Pydantic ----------------------
class FoodCreate(BaseModel):
    name: str
    calories_per_serving: float
    carbs_per_serving: float
    fats_per_serving: float
    protein_per_serving: float
    food_url: str


class FoodResponse(BaseModel):
    id: int
    name: str
    calories_per_serving: float
    carbs_per_serving: float
    fats_per_serving: float
    protein_per_serving: float
    food_url: str


# ----------------------  Agregar alimento a una comida ----------------------
@router.post('/food}', status_code=status.HTTP_201_CREATED)
async def add_food_to_meal(
    food: FoodCreate,
    db: DBSession,
    current_user: AutoAdminUser,  # noqa: ARG001
) -> FoodResponse:

    new_food = Food(
        name=food.name,
        calories_per_serving=food.calories_per_serving,
        carbs_per_serving=food.carbs_per_serving,
        fats_per_serving=food.fats_per_serving,
        protein_per_serving=food.protein_per_serving
    )
    db.add(new_food)
    db.commit()
    db.refresh(new_food)
    return new_food


# ---------------------- Ver alimentos de una comida ----------------------
@router.get('/')
async def get_foods_by_meal(
    db: DBSession,
    current_user: AutoAdminUser,  # noqa: ARG001
) -> list[type[Food]]:
    return db.query(Food).all()
