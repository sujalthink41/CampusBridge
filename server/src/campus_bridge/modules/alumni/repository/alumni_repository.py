from uuid import UUID

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from campus_bridge.data.database.session import get_async_session
from campus_bridge.data.models import User
from campus_bridge.data.models.alumni import Alumni
from campus_bridge.errors.decorators.sqlalchemy import sqlalchemy_exceptions


class AlumniRepository:

    def __init__(self, db: AsyncSession):
        self.db = db

    @sqlalchemy_exceptions
    async def get_current_alumni(self, user_id: UUID) -> Alumni:
        """Get the current alumni profile"""
        alumni = await self.db.execute(select(Alumni).where(Alumni.user_id == user_id))
        return alumni.scalar_one_or_none()

    @sqlalchemy_exceptions
    async def get_all_alumni(self) -> list[Alumni]:
        """Get all alumni profiles"""
        alumni = await self.db.execute(select(Alumni))
        return alumni.scalars().all()

    @sqlalchemy_exceptions
    async def get_all_alumni_by_college(
        self, college_id: UUID | None = None, skip: int = 0, limit: int = 100
    ) -> list[Alumni]:
        """Get all alumni, optionally filtered by college_id"""
        stmt = select(Alumni)

        if college_id:
            stmt = stmt.join(User).where(
                User.college_id == college_id,
            )

        stmt = stmt.offset(skip).limit(limit)
        alumni = await self.db.execute(stmt)
        return alumni.scalars().all()

    @sqlalchemy_exceptions
    async def create_alumni(self, alumni: Alumni) -> Alumni:
        """Create a new alumni profile"""
        self.db.add(alumni)
        await self.db.commit()
        await self.db.refresh(alumni)
        return alumni

    @sqlalchemy_exceptions
    async def update_alumni(self, alumni: Alumni) -> Alumni:
        """Update an alumni profile"""
        await self.db.flush()
        await self.db.refresh(alumni)
        return alumni

    @sqlalchemy_exceptions
    async def delete_alumni(self, alumni_id: UUID) -> None:
        """Delete an alumni profile"""
        await self.db.execute(delete(Alumni).where(Alumni.id == alumni_id))
        await self.db.commit()


def get_alumni_repository(
    db: AsyncSession = Depends(get_async_session),
) -> AlumniRepository:
    return AlumniRepository(db)
