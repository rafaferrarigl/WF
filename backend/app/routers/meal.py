from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from app.database import DBSession
from app.models.food_meal import FoodMeal
from app.models.meal import Meal
from app.routers.auth import AutoAdminUser
from app.routers.food import FoodData

router = APIRouter(prefix="/meals", tags=["diets"])


class FoodMealResponse(BaseModel):
    id: int
    food: FoodData
    servings: int
    model_config = {"from_attributes": True}


class MealResponse(BaseModel):
    id: int
    name: str
    foods: list[FoodMealResponse] = []
    model_config = {"from_attributes": True}


class MealCreate(BaseModel):
    name: str
    description: str | None = None


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=MealResponse)
async def create_meal(
    meal: MealCreate,
    db: DBSession,
    current_user: AutoAdminUser
):
    new_meal = Meal(
        name=meal.name,
        description=meal.description
    )
    db.add(new_meal)
    db.commit()
    db.refresh(new_meal)

    return MealResponse(
        id=new_meal.id,
        name=new_meal.name,
        foods=[]
    )

# ---------------------- Ver todas las meals ----------------------
@router.get("/", response_model=list[MealResponse])
async def get_all_meals(db: DBSession, current_user: AutoAdminUser):
    meals = db.query(Meal).all()
    response = []

    for meal in meals:
        foods_in_meal = [
            FoodMealResponse(
                id=fm.id,
                food=FoodData.model_validate(fm.food),
                servings=fm.servings
            )
            for fm in meal.food_meals
        ]

        response.append(MealResponse(
            id=meal.id,
            name=meal.name,
            foods=foods_in_meal
        ))

    return response
