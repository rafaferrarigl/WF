
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel

from app.database import DBSession  # noqa: TC001
from app.models import routine_exercise as routine_exercise_model
from app.models.exercise import Exercise
from app.models.routine import Routine
from app.models.user import User
from app.routers.auth import AutoAdminUser, AutoUser  # noqa: TC001
from app.routers.exercises import ExerciseResponse  # noqa: TC001



router = APIRouter(
    prefix="/exercise_routines",
    tags=["routines"],
)

class RoutineExerciseCreate(BaseModel):
    routine_id: int
    exercise_id: int
    min_repeats: int
    max_repeats: int
    sets: int


