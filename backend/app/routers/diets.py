from __future__ import annotations

from datetime import UTC, datetime

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import joinedload

from app.database import DBSession  # noqa: TC001
from app.models.diet import Diet
from app.models.meal import Meal
from app.models.user import User
from app.routers.meal import FoodMealResponse
from app.routers.meal import FoodData
from app.routers.auth import AutoAdminUser, AutoUser  # noqa: TC001
from app.routers.meal import MealResponse

router = APIRouter(
    prefix='/diets',
    tags=['diets'],
)


class DietResponse(BaseModel):
    id: int
    name: str
    trainer_id: int
    client_id: int
    created_at: datetime
    meals: list[MealResponse] = []
    model_config = {"from_attributes": True}


class DietCreate(BaseModel):
    name: str
    client_id: int
    meal_ids: list[int] = []
    model_config = {"from_attributes": True}


# ---------------------- Crear dieta (solo entrenadores) ----------------------
@router.post('/', status_code=status.HTTP_201_CREATED)
async def create_diet(
        diet_request: DietCreate,
        db: DBSession,
        current_user: AutoAdminUser,
) -> DietResponse:
    # Verificar que el cliente exista
    client = db.query(User).filter(User.id == diet_request.client_id).first()
    if not client:
        raise HTTPException(status_code=404, detail='Cliente no encontrado.')

    new_diet = Diet(
        name=diet_request.name,
        trainer_id=current_user.user_id,
        client_id=diet_request.client_id,
        created_at=datetime.now(UTC),
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


# ---------------------- Ver todas las dietas ----------------------
@router.get('/')
async def get_all_diets(
        db: DBSession,
        current_user: AutoUser,
) -> list[DietResponse]:
    filter_element = Diet.trainer_id if current_user.is_admin else Diet.client_id
    diets = (db.query(Diet)).all()
    response = []
    for diet in diets:
        meals_response = []

        for meal in diet.meals:
            foods_in_meal = [
                FoodMealResponse(
                    id=fm.id,
                    servings=fm.servings,
                    food=FoodData.model_validate(fm.food)
                )
                for fm in meal.food_meals
            ]

            meals_response.append(MealResponse(
                id=meal.id,
                name=meal.name,
                foods=foods_in_meal
            ))

        response.append(DietResponse(
            id=diet.id,
            name=diet.name,
            trainer_id=diet.trainer_id,
            client_id=diet.client_id,
            created_at=diet.created_at,
            meals=meals_response
        ))

    return response



#ToDo: Get diet by id

# ---------------------- Ver una dieta específica ----------------------
#
# @router.get('/{diet_id}')
# async def get_diet(
#         diet_id: int,
#         db: DBSession,
#         current_user: AutoUser,
# ) -> DietResponse:
#     diet = db.query(Diet).options(joinedload(Diet.meals).joinedload(Meal.foods)).filter(Diet.id == diet_id).first()
#     if not diet:
#         raise HTTPException(status_code=404, detail='Dieta no encontrada.')
#
#     # Solo el entrenador o el cliente asignado pueden verla
#     if not (
#             (current_user.is_admin and diet.trainer_id == current_user.user_id)
#             or (not current_user.is_admin and diet.client_id == current_user.user_id)
#     ):
#         raise HTTPException(status_code=403, detail='No tienes permiso para ver esta dieta.')
#
#     return diet
