from fastapi import FastAPI, HTTPException, Depends, status
from typing import Annotated
from app.database import engine, SessionLocal, Base
from app.models import user
from app.models.routine import Routine
from app.models.exercise import Exercise
from app.models.exercise_progress import ExerciseProgress
from app.models.diet import Diet
from app.models.meal import Meal
from app.models.food import Food
from app.routers import auth
from app.routers.auth import get_current_user
from app.routers import routines
from app.routers import exercises
from app.routers import diets
from app.routers import meal
from app.routers import food
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()
app.include_router(auth.router)
app.include_router(routines.router)
app.include_router(diets.router)
app.include_router(exercises.router)
app.include_router(meal.router)
app.include_router(food.router)

Base.metadata.create_all(bind=engine)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # 👈 tu frontend Vite
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]


@app.get("/auth/me", tags=["auth"])
async def get_me(user: user_dependency):
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user  # 👈 devolvemos el user directamente, sin el wrapper {"User": ...}
