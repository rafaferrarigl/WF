from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Annotated, List
from datetime import datetime
from pydantic import BaseModel, Field

from app.database import SessionLocal
from app.models.diet import Diet
from app.models.user import User
from app.routers.auth import get_current_user


router = APIRouter(
    prefix="/diets",
    tags=["diets"]
)

# ---------------------- 🔧 Dependencia DB ----------------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]


# ---------------------- 📦 Esquemas Pydantic ----------------------

class DietCreate(BaseModel):
    name: str = Field(..., example="Dieta de definición - Semana 1")
    description: str | None = Field(None, example="Alta en proteínas, baja en carbohidratos")
    client_id: int = Field(..., example=3)


class DietResponse(BaseModel):
    id: int
    name: str
    description: str | None
    created_at: datetime
    trainer_id: int
    client_id: int

    class Config:
        orm_mode = True


# ---------------------- 👨‍🏫 Crear dieta (solo entrenadores) ----------------------
@router.post("/", response_model=DietResponse, status_code=status.HTTP_201_CREATED)
async def create_diet(
    diet_request: DietCreate,
    db: db_dependency,
    current_user=Depends(get_current_user)
):
    # 🚫 Solo los entrenadores pueden crear dietas
    if not current_user["is_admin"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Solo los entrenadores pueden crear dietas."
        )

    # ✅ Verificar que el cliente exista
    client = db.query(User).filter(User.id == diet_request.client_id).first()
    if not client:
        raise HTTPException(status_code=404, detail="Cliente no encontrado.")

    new_diet = Diet(
        name=diet_request.name,
        description=diet_request.description,
        trainer_id=current_user["id"],
        client_id=diet_request.client_id,
        created_at=datetime.utcnow()
    )

    db.add(new_diet)
    db.commit()
    db.refresh(new_diet)

    return new_diet


# ---------------------- 👀 Ver todas las dietas ----------------------
@router.get("/", response_model=List[DietResponse])
async def get_all_diets(
    db: db_dependency,
    current_user=Depends(get_current_user)
):
    # 🧠 Entrenadores ven las dietas que crearon
    if current_user["is_admin"]:
        diets = db.query(Diet).filter(Diet.trainer_id == current_user["id"]).all()
    else:
        # 🏋️ Clientes ven solo las suyas
        diets = db.query(Diet).filter(Diet.client_id == current_user["id"]).all()

    return diets


# ---------------------- 🔎 Ver una dieta específica ----------------------
@router.get("/{diet_id}", response_model=DietResponse)
async def get_diet(
    diet_id: int,
    db: db_dependency,
    current_user=Depends(get_current_user)
):
    diet = db.query(Diet).filter(Diet.id == diet_id).first()
    if not diet:
        raise HTTPException(status_code=404, detail="Dieta no encontrada.")

    # ⚖️ Solo el entrenador o el cliente asignado pueden verla
    if not (
        current_user["is_admin"] and diet.trainer_id == current_user["id"]
    ) and not (
        not current_user["is_admin"] and diet.client_id == current_user["id"]
    ):
        raise HTTPException(status_code=403, detail="No tienes permiso para ver esta dieta.")

    return diet
