import logging

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy_utils import database_exists, create_database
from sqlmodel import Session, select

from app.core.config import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def init(db_engine: Engine) -> None:
    if not database_exists(db_engine.url):
        create_database(db_engine.url)
    try:
        with Session(db_engine) as session:  # type: ignore[attr-defined]
            # Try to create session to check if DB is awake
            session.exec(select(1))
    except Exception as e:
        logger.error(e)
        raise


def main() -> None:
    logger.info("Initializing service")
    db_engine = create_engine(str(settings.SQLALCHEMY_DATABASE_URI))
    init(db_engine)
    logger.info("Service finished initializing")


if __name__ == "__main__":
    main()
