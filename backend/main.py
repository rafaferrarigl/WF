from fastapi import FastAPI, HTTPException, Depends, status
from typing import Annotated
from app.database import engine, SessionLocal
from app.models import user
from sqlalchemy.orm import Session
from app.routers import auth
from app.routers.auth import get_current_user
from app.routers import routines

app = FastAPI()
app.include_router(auth.router)
app.include_router(routines.router)

user.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]


@app.get("/", status_code=status.HTTP_200_OK, tags=["user"])
async def user(user:user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return {"User": user}