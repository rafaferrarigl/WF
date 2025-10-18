# app/routers/auth.py

from datetime import datetime, timedelta, date
from typing import Annotated
from fastapi import Depends, HTTPException, APIRouter
from pydantic import BaseModel
from sqlalchemy.orm import Session
from starlette import status
from app.database import SessionLocal
from app.models.user import User
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
import os
from dotenv import load_dotenv


# -------------------------------------------------------------------
# 🔧 Configuración básica
# -------------------------------------------------------------------
router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="auth/login")


# -------------------------------------------------------------------
# 📦 Modelos Pydantic
# -------------------------------------------------------------------
class CreateUserRequest(BaseModel):
    username: str
    email: str
    password: str
    is_admin: bool = False  # 👈 campo opcional (por defecto False)
    birth_date: date | None = None
    height: float | None = None
    weight: float | None = None


class Token(BaseModel):
    access_token: str
    token_type: str


# -------------------------------------------------------------------
# 🗄️ Dependencia de DB
# -------------------------------------------------------------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]


# -------------------------------------------------------------------
# 👤 Crear nuevo usuario
# -------------------------------------------------------------------
@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(db: db_dependency, create_user_request: CreateUserRequest):
    existing_user = db.query(User).filter(
        (User.username == create_user_request.username)
        | (User.email == create_user_request.email)
    ).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username or email already registered.",
        )

    create_user_model = User(
    username=create_user_request.username,
    email=create_user_request.email,
    password=bcrypt_context.hash(create_user_request.password),
    is_admin=create_user_request.is_admin,
    birth_date=create_user_request.birth_date,
    height=create_user_request.height,
    weight=create_user_request.weight
    )


    db.add(create_user_model)
    db.commit()
    db.refresh(create_user_model)

    return {"message": f"User '{create_user_model.username}' created successfully."}


# -------------------------------------------------------------------
# 🔐 Login
# -------------------------------------------------------------------
@router.post("/login", response_model=Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: db_dependency
):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = create_access_token(
        username=user.username,
        user_id=user.id,
        is_admin=user.is_admin,
        expires_delta=timedelta(minutes=30)
    )

    return {"access_token": token, "token_type": "bearer"}


# -------------------------------------------------------------------
# 🔑 Funciones auxiliares
# -------------------------------------------------------------------
def authenticate_user(username: str, password: str, db: Session):
    user = db.query(User).filter(User.username == username).first()
    if not user:
        return False
    if not bcrypt_context.verify(password, user.password):
        return False
    return user


def create_access_token(username: str, user_id: int, is_admin: bool, expires_delta: timedelta):
    encode = {"sub": username, "id": user_id, "is_admin": is_admin}
    expire = datetime.utcnow() + expires_delta
    encode.update({"exp": expire})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)


# -------------------------------------------------------------------
# 🧠 Obtener usuario actual desde el token
# -------------------------------------------------------------------
async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        user_id: int = payload.get("id")
        is_admin: bool = payload.get("is_admin")
        expire_date = payload.get("exp")

        if datetime.utcnow() > datetime.utcfromtimestamp(expire_date):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token has expired",
                headers={"WWW-Authenticate": "Bearer"},
            )

        if username is None or user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )

        return {"username": username, "id": user_id, "is_admin": is_admin}

    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


# -------------------------------------------------------------------
# 🛡️ Dependencia para rutas protegidas solo para admins
# -------------------------------------------------------------------
def admin_required(current_user: dict = Depends(get_current_user)):
    if not current_user["is_admin"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to perform this action.",
        )
    return current_user
