import logging
from typing import Any, Dict, List, Optional, Union

from sqlalchemy import (
    CursorResult,
    Delete,
    Insert,
    MetaData,
    NullPool,
    Select,
    Update,
)
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import create_async_engine

from app.settings import sqlalchemy_settings

logger = logging.getLogger(__name__)

DATABASE_URL = str(sqlalchemy_settings.POSTGRES_DATABASE_URL)
logging.info("Postgress Database_URL: %s", DATABASE_URL)
engine = create_async_engine(DATABASE_URL, poolclass=NullPool)

DB_NAMING_CONVENTION = {
    "ix": "%(column_0_label)s_idx",
    "uq": "%(table_name)s_%(column_0_name)s_key",
    "ck": "%(table_name)s_%(constraint_name)s_check",
    "fk": "%(table_name)s_%(column_0_name)s_fkey",
    "pk": "%(table_name)s_pkey",
}

metadata = MetaData(naming_convention=DB_NAMING_CONVENTION)


async def drop_tables():
    pass


async def create_tables(drop_before=True):
    logger.info(
        f"Creating all tables in {metadata.sorted_tables}, using engien: {engine.url}"
    )
    async with engine.begin() as conn:
        if drop_before:
            await conn.run_sync(metadata.drop_all)
        await conn.run_sync(metadata.create_all)
    logger.info("Finished creating tables")


async def fetch_one(
    query: Union[Select, Insert, Update, Delete],
) -> Optional[Dict[str, Any]]:
    try:
        async with engine.begin() as conn:
            cursor: CursorResult = await conn.execute(query)
            return cursor.first()._asdict() if cursor.rowcount > 0 else None
    except SQLAlchemyError as e:
        logger.error(f"Error executing query: {e}")
        raise


async def fetch_all(query: Select) -> List[Dict[str, Any]]:
    try:
        async with engine.begin() as conn:
            cursor: CursorResult = await conn.execute(query)
            return [r._asdict() for r in cursor.all()]
    except SQLAlchemyError as e:
        logger.error(f"Error executing query: {e}")
        raise


async def execute(query: Union[Insert, Update, Delete]) -> None:
    try:
        async with engine.begin() as conn:
            await conn.execute(query)
    except SQLAlchemyError as e:
        logger.error(f"Error executing query: {e}")
        raise
