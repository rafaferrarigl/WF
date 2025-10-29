from __future__ import annotations

from os import environ

import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database import Base, set_db
from app.routers import auth, diets, exercises, food, meal, routines
from app.routers.auth import user_dependency  # noqa: TC001
from app.routers.routines import RoutineResponse


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
async def get_me(user: user_dependency):
    if user is None:
        raise HTTPException(status_code=404, detail='User not found')
    return user


def main() -> None:
    engine = create_engine(environ['DATABASE_URL'])
    sm = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    set_db(sm)
    Base.metadata.create_all(bind=engine)

    RoutineResponse.model_rebuild()
    app.openapi()
    uvicorn.run(app, host='localhost', port=8000)


if __name__ == '__main__':
    main()
