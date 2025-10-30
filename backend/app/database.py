from __future__ import annotations

from typing import TYPE_CHECKING, Annotated, Any

from fastapi import Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, declarative_base, sessionmaker


if TYPE_CHECKING:
    from collections.abc import Generator


class Database:
    base = declarative_base()
    _session_maker: sessionmaker

    @classmethod
    def init(cls, db_url: str) -> None:
        engine = create_engine(db_url)
        cls._session_maker = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        cls.base.metadata.create_all(bind=engine)

    @classmethod
    def get_session(cls) -> Generator[Session | Any, Any, None]:
        db = cls._session_maker()
        try:
            yield db
        finally:
            db.close()


DBSession = Annotated[Session, Depends(Database.get_session)]
