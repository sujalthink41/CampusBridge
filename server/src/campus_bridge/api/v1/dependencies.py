from typing import AsyncGenerator
import structlog
from sqlalchemy.ext.asyncio import AsyncSession

from campus_bridge.data.database.core import AsyncSessionLocal

logger = structlog.stdlib.get_logger(__name__)

async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception as exc:
            logger.exception("Database transaction failed", exc=exc)
            await session.rollback()
            raise
