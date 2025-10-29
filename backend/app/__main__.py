from __future__ import annotations

from typing import Annotated

import uvicorn
from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from app.database import Base, SessionLocal, engine
from app.routers import auth, diets, exercises, food, meal, routines
from app.routers.auth import get_current_user


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
    allow_origins=['http://localhost:5173'],  # 👈 tu frontend Vite
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]


@app.get('/auth/me', tags=['auth'])
async def get_me(user: user_dependency):
    if user is None:
        raise HTTPException(status_code=404, detail='User not found')
    return user  # 👈 devolvemos el user directamente, sin el wrapper {"User": ...}


if __name__ == '__main__':
    uvicorn.run(app, host='localhost', port=8000)
