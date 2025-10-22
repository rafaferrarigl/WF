from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Annotated, List
from pydantic import BaseModel
from app.database import SessionLocal
from app.models.food import Food
from app.models.meal import Meal
from app.routers.auth import get_current_user

router = APIRouter(prefix="/foods", tags=["diets"])

# ---------------------- 🔧 Dependencia DB ----------------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]


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

    class Config:
        orm_mode = True


# ---------------------- 🧑‍🍳 Agregar alimento a una comida ----------------------
@router.post("/meal/{meal_id}", response_model=FoodResponse, status_code=status.HTTP_201_CREATED)
async def add_food_to_meal(
    meal_id: int,
    food: FoodCreate,
    db: db_dependency,
    current_user=Depends(get_current_user)
):
    # Solo entrenadores pueden agregar alimentos
    if not current_user["is_admin"]:
        raise HTTPException(status_code=403, detail="Solo entrenadores pueden agregar alimentos.")

    meal = db.query(Meal).filter(Meal.id == meal_id).first()
    if not meal:
        raise HTTPException(status_code=404, detail="Comida no encontrada.")

    new_food = Food(
        name=food.name,
        grams=food.grams,
        protein=food.protein,
        carbs=food.carbs,
        fats=food.fats,
        meal_id=meal.id
    )
    db.add(new_food)
    db.commit()
    db.refresh(new_food)
    return new_food


# ---------------------- 👀 Ver alimentos de una comida ----------------------
@router.get("/meal/{meal_id}", response_model=List[FoodResponse])
async def get_foods_by_meal(
    meal_id: int,
    db: db_dependency,
    current_user=Depends(get_current_user)
):
    foods = db.query(Food).filter(Food.meal_id == meal_id).all()
    return foods
