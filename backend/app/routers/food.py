from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from fatsecret import Fatsecret
from os import environ
from app.database import DBSession
from app.models.food import Food
from app.models.food_meal import FoodMeal
from app.models.meal import Meal
from app.routers.auth import AutoAdminUser

router = APIRouter(prefix="/foods", tags=["diets"])

consumer_key = environ['CONSUMER_KEY']
consumer_secret = environ['CONSUMER_SECRET']
fs = Fatsecret(consumer_key, consumer_secret)


class FoodSearchRequest(BaseModel):
    query: str


class FoodData(BaseModel):
    id: int
    name: str
    serving: str
    calories: float
    fats: float
    carbs: float
    protein: float
    url: str

    model_config = {"from_attributes": True}

    @classmethod
    def from_description(cls, data: dict, food_description: str):
        serving, contents = food_description.split(" - ", maxsplit=1)
        contents = contents.split(" | ", maxsplit=3)
        return cls(
            id=int(data['food_id']),
            name=data['food_name'],
            url=data['food_url'],
            serving=serving,
            calories=float(contents[0][10:-4]),
            fats=float(contents[1][5:-1]),
            carbs=float(contents[2][7:-1]),
            protein=float(contents[3][9:-1])
        )


class FoodDataForAdd(FoodData):
    servings: int


# ---------------------- SEARCH ----------------------
@router.post("/search", response_model=list[FoodData])
async def search_foods(req: FoodSearchRequest):
    results = fs.foods_search(req.query)
    if not results:
        raise HTTPException(404, "No se encontraron alimentos.")

    return [FoodData.from_description(f, f['food_description']) for f in results]


# ---------------------- ADD FOOD TO MEAL ----------------------
@router.post("/meal/{meal_id}")
async def add_food_to_meal(
        meal_id: int,
        food_data: FoodDataForAdd,
        db: DBSession,
        current_user: AutoAdminUser
):
    meal = db.query(Meal).filter(Meal.id == meal_id).first()
    if not meal:
        raise HTTPException(status_code=404, detail='Comida no encontrada.')

    food = db.query(Food).filter(Food.name == food_data.name).first()
    if not food:
        food = Food(
            name=food_data.name,
            serving=food_data.serving,
            calories=food_data.calories,
            carbs=food_data.carbs,
            fats=food_data.fats,
            protein=food_data.protein,
            url=food_data.url
        )
        db.add(food)
        db.commit()
        db.refresh(food)

    # Crear relación con Meal
    food_meal = FoodMeal(
        meal_id=meal_id,
        food_id=food.id,
        servings=food_data.servings
    )
    db.add(food_meal)
    db.commit()

    return {"message": "Food added", "food_id": food.id}
