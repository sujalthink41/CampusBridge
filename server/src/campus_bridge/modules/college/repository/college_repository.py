from typing import Optional
from uuid import UUID

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from campus_bridge.data.database.session import get_async_session
from campus_bridge.data.models.college import College
from campus_bridge.errors.decorators.sqlalchemy import sqlalchemy_exceptions


class CollegeRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    @sqlalchemy_exceptions
    async def create_colleges(self, colleges: list[College]) -> list[College]:
        """Create a single or multiple college at a time"""
        self.db.add_all(colleges)
        await self.db.flush()

        for college in colleges:
            await self.db.refresh(college)

        return colleges

    @sqlalchemy_exceptions
    async def get_college_by_id(
        self,
        college_id: UUID,
    ) -> College | None:
        """Get a college by id or get all"""
        result = await self.db.execute(
            select(College).where(College.id == college_id, ~College.is_deleted)
        )
        return result.scalar_one_or_none()

    @sqlalchemy_exceptions
    async def get_all_college(self) -> list[College]:
        """Get all college"""
        result = await self.db.execute(select(College).where(~College.is_deleted))
        return result.scalars().all()

    @sqlalchemy_exceptions
    async def update_college(self, college: College) -> College:
        """Partially update college"""
        await self.db.flush()
        await self.db.refresh(college)
        return college

    @sqlalchemy_exceptions
    async def delete_college(self, college: College) -> None:
        """Soft delete a college"""
        college.is_deleted = True
        await self.db.flush()


def get_college_repository(
    db: AsyncSession = Depends(get_async_session),
) -> CollegeRepository:
    return CollegeRepository(db=db)
