from __future__ import annotations

from typing import TYPE_CHECKING

import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from app.database import Base, engine
from app.routers import auth, diets, exercises, food, meal, routines


if TYPE_CHECKING:
    from app.routers.auth import user_dependency


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


@app.get('/auth/me', tags=['auth'])
async def get_me(user: user_dependency):
    if user is None:
        raise HTTPException(status_code=404, detail='User not found')
    return user  # 👈 devolvemos el user directamente, sin el wrapper {"User": ...}


if __name__ == '__main__':
    uvicorn.run(app, host='localhost', port=8000)
