from __future__ import annotations

from os import environ

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import Database
from app.routers import auth, diets, exercises, food, meal, routines
from app.routers.auth import AutoUser  # noqa: TC001


app = FastAPI()
app.include_router(auth.router)
app.include_router(routines.router)
app.include_router(diets.router)
app.include_router(exercises.router)
app.include_router(meal.router)
app.include_router(food.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://localhost:5173'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)


@app.get('/auth/me', tags=['auth'])
async def get_me(user: AutoUser) -> AutoUser:
    return user


def main() -> None:
    db_user = environ['DB_USER']
    db_pass = environ['DB_PASS']
    db_name = environ['DB_NAME']

    Database.init(f'postgresql://{db_user}:{db_pass}@database:5432/{db_name}')

    uvicorn.run(app, host='0.0.0.0', port=8000)


if __name__ == '__main__':
    main()
