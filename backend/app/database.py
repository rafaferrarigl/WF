from __future__ import annotations

from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session, declarative_base, sessionmaker


Base = declarative_base()
_session: sessionmaker


def set_db(session: sessionmaker) -> None:
    global _session
    _session = session


def get_db():
    db = _session()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]
