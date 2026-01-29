from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession

import structlog

from campus_bridge.data.database.core import AsyncSessionLocal

logger = structlog.stdlib.get_logger(__name__)

async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    """Dependency to get async database session"""
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception as exc:
            logger.exception("Database transaction failed", exc=exc)
            await session.rollback()
            raise
