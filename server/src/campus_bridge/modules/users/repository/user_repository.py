from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from fastapi import Depends

from campus_bridge.api.v1.dependencies import get_async_session
from campus_bridge.data.models.user import User
from campus_bridge.errors.decorators.sqlalchemy import sqlalchemy_exceptions


class UserRepository:
    def __init__(
        self,
        db: AsyncSession
    ):
        self.db = db 

    @sqlalchemy_exceptions
    async def get_user_by_id(self, user_id: str | UUID) -> User | None:
        """Fetch user by id"""
        result = await self.db.execute(
            select(User).where(
                User.id == user_id, 
                User.is_deleted.is_(False)
            )
        )
        return result.scalar_one_or_none()


def get_user_repository(
    db: AsyncSession = Depends(get_async_session)
) -> UserRepository:
    return UserRepository(db)