from __future__ import annotations

import os
from datetime import UTC, date, datetime, timedelta
from typing import TYPE_CHECKING, Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel
from starlette import status

from app.database import db_dependency  # noqa: TC001
from app.models.user import User


if TYPE_CHECKING:
    from sqlalchemy.orm import Session

# -------------------------------------------------------------------
# 🔧 Configuración básica
# -------------------------------------------------------------------
router = APIRouter(
    prefix='/auth',
    tags=['auth'],
)

SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = os.getenv('ALGORITHM')

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth2_bearer = OAuth2PasswordBearer(tokenUrl='auth/login')


# -------------------------------------------------------------------
# 📦 Modelos Pydantic
# -------------------------------------------------------------------
class CreateUserRequest(BaseModel):
    username: str
    email: str
    password: str
    is_admin: bool = False
    birth_date: date | None = None
    height: float | None = None
    weight: float | None = None
    gender: str | None = None


class Token(BaseModel):
    access_token: str
    token_type: str


# -------------------------------------------------------------------
# 👤 Crear nuevo usuario
# -------------------------------------------------------------------
@router.post('/', status_code=status.HTTP_201_CREATED)
async def create_user(db: db_dependency, create_user_request: CreateUserRequest):
    existing_user = (
        db.query(User)
        .filter(
            (User.username == create_user_request.username) | (User.email == create_user_request.email),
        )
        .first()
    )
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Username or email already registered.',
        )
    create_user_model = User(
        username=create_user_request.username,
        email=create_user_request.email,
        hashed_password=bcrypt_context.hash(create_user_request.password),
        is_admin=create_user_request.is_admin,
        birth_date=create_user_request.birth_date,
        height=create_user_request.height,
        weight=create_user_request.weight,
        gender=create_user_request.gender,
    )

    db.add(create_user_model)
    db.commit()
    db.refresh(create_user_model)

    return {'message': f"User '{create_user_model.username}' created successfully."}


# -------------------------------------------------------------------
# 🔐 Login
# -------------------------------------------------------------------
@router.post('/login', response_model=Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: db_dependency,
):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Incorrect username or password',
            headers={'WWW-Authenticate': 'Bearer'},
        )
    token = create_access_token(
        username=user.username,  # type: ignore[bad-argument-type]
        user_id=user.id,  # type: ignore[bad-argument-type]
        is_admin=user.is_admin,  # type: ignore[bad-argument-type]
        expires_delta=timedelta(minutes=30),
    )

    return {'access_token': token, 'token_type': 'bearer'}


# -------------------------------------------------------------------
# 🔑 Funciones auxiliares
# -------------------------------------------------------------------
def authenticate_user(username: str, password: str, db: Session):
    user = db.query(User).filter(User.username == username).first()
    if not user:
        return False
    if not bcrypt_context.verify(password, user.hashed_password):
        return False
    return user


def create_access_token(username: str, user_id: int, is_admin: bool, expires_delta: timedelta):
    encode = {'sub': username, 'id': user_id, 'is_admin': is_admin}
    expire = datetime.now(UTC) + expires_delta
    encode.update({'exp': int(expire.timestamp())})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)


# -------------------------------------------------------------------
# 🧠 Obtener usuario actual desde el token
# -------------------------------------------------------------------
async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Could not validate credentials',
            headers={'WWW-Authenticate': 'Bearer'},
        )

    username = payload.get('sub')
    user_id = payload.get('id')
    is_admin = payload.get('is_admin')
    expire_date = payload.get('exp', datetime.now(UTC).timestamp())

    if username is None or user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Could not validate credentials',
            headers={'WWW-Authenticate': 'Bearer'},
        )

    if datetime.now(UTC) > datetime.fromtimestamp(expire_date, UTC):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Token has expired',
            headers={'WWW-Authenticate': 'Bearer'},
        )

    return {'username': username, 'id': user_id, 'is_admin': is_admin}


async def assert_admin_user(token: Annotated[str, Depends(oauth2_bearer)]):
    user = await get_current_user(token)
    if not user['is_admin']:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='You do not have permission to perform this action.',
        )

    return user


AutoUser = Annotated[dict, Depends(get_current_user)]
AutoAdminUser = Annotated[dict, Depends(assert_admin_user)]
