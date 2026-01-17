from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from fastapi import Depends

from campus_bridge.data.models.user import User
from campus_bridge.api.v1.dependencies import get_async_session
from campus_bridge.errors.decorators.sqlalchemy import sqlalchemy_exceptions

class AuthRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    @sqlalchemy_exceptions
    async def get_by_email(self, email: str) -> User | None:
        """Get a single user by their email id"""
        result = await self.db.execute(
            select(User).where(User.email == email)
        )
        return result.scalar_one_or_none()

    @sqlalchemy_exceptions
    async def create(self, user: User) -> User:
        """Create a singe user"""
        self.db.add(user)
        await self.db.flush()   
        await self.db.refresh(user)
        return user


def get_auth_repository(
    db: AsyncSession = Depends(get_async_session),
) -> AuthRepository:
    return AuthRepository(db)