from __future__ import annotations

import os
from pathlib import Path
from typing import TYPE_CHECKING, Annotated, Any

from alembic.command import upgrade
from alembic.config import Config
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

        alembic_path = os.path.join(os.getcwd(), "alembic", "alembic.ini")
        config = Config(alembic_path)

        # Ajustar el script_location si es necesario
        config.set_main_option("script_location", "alembic/alembic")
        config.set_main_option("sqlalchemy.url", db_url.replace('%', '%%'))

        upgrade(config, 'head')

    @classmethod
    def get_session(cls) -> Generator[Session | Any, Any, None]:
        db = cls._session_maker()
        try:
            yield db
        finally:
            db.close()


DBSession = Annotated[Session, Depends(Database.get_session)]
