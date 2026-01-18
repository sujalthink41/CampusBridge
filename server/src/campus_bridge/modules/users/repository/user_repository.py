from uuid import UUID
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from fastapi import Depends

from campus_bridge.api.v1.dependencies import get_async_session
from campus_bridge.data.models.user import User
from campus_bridge.data.models.college import College
from campus_bridge.data.enums.role import RoleEnum
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
                ~User.is_deleted()
            )
        )
        return result.scalar_one_or_none()

    @sqlalchemy_exceptions
    async def get_all_users_by_college_id_or_role(self, college_id: UUID, role: Optional[RoleEnum] = None) -> list[User]:
        """Fetch all users under a particular college, optionally filtered by role"""
        query = select(User).where(
            User.college_id == college_id,
            ~User.is_deleted()
        )
        
        if role is not None:
            query = query.where(User.role == role)
        
        result = await self.db.execute(query)
        return result.scalars().all()


def get_user_repository(
    db: AsyncSession = Depends(get_async_session)
) -> UserRepository:
    return UserRepository(db)