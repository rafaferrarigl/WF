from __future__ import annotations

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel

from app.database import DBSession  # noqa: TC001
from app.models.food import Food
from app.models.food_meal import FoodMeal
from app.models.meal import Meal
from app.routers.auth import AutoAdminUser  # noqa: TC001
from app.routers.food import FoodResponse

router = APIRouter(
    prefix='/meals',
    tags=['diets']
)


# ----------------------  Esquemas Pydantic ----------------------



class FoodMealCreate(BaseModel):
    food_id: int
    servings: int

class MealCreate(BaseModel):
    name: str
    description: str | None = None
    foods: list[FoodMealCreate] = []

class FoodMealResponse(BaseModel):
    id: int
    food: FoodResponse
    servings: int
    model_config = {"from_attributes": True}

class MealResponse(BaseModel):
    id: int
    name: str
    foods: list[FoodMealResponse] = []
    model_config = {"from_attributes": True}

# ----------------------Crear comida----------------------
@router.post('/', status_code=status.HTTP_201_CREATED)
async def create_meal(
    meal: MealCreate,
    db: DBSession,
    current_user: AutoAdminUser,  # noqa: ARG001
) -> MealResponse:
    new_meal = Meal(
        name=meal.name,
        description=meal.description,

    )
    db.add(new_meal)
    db.commit()
    db.refresh(new_meal)

    for fd in meal.foods:

        foods = db.query(Food).filter(Food.id == fd.food_id).first()
        if not foods:
            raise HTTPException(
                status_code=404,
                detail=f'Comida {fd.food_id} no encontrada'
            )

        meal_fd = FoodMeal(
            meal_id=new_meal.id,
            food_id=fd.food_id,
            servings=fd.servings,
        )

        db.add(meal_fd)

    db.commit()
    db.refresh(new_meal)



    return new_meal


# ----------------------Ver todas las comidas ----------------------
@router.get('/')
async def get_all_meals(
    db: DBSession,
    current_user: AutoAdminUser,  # noqa: ARG001
) -> list[MealResponse]:
    return db.query(Meal).all()




#ToDo
# ---------------------- Ver una comida específica ----------------------
# @router.get('/{meal_id}')
# async def get_meal(
#     meal_id: int,
#     db: DBSession,
#     current_user: AutoAdminUser,  # noqa: ARG001
# ) -> MealResponse:
#     meal = db.query(Meal).filter(Meal.id == meal_id).first()
#     if not meal:
#         raise HTTPException(status_code=404, detail='Comida no encontrada.')
#     return meal
