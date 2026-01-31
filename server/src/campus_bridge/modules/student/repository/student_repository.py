from uuid import UUID

from fastapi import Depends
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from campus_bridge.data.database.session import get_async_session
from campus_bridge.data.models import User
from campus_bridge.data.models.student import Student
from campus_bridge.errors.decorators.sqlalchemy import sqlalchemy_exceptions


class StudentRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    @sqlalchemy_exceptions
    async def get_by_user_id(self, user_id: UUID) -> Student:
        """Get a student by user id"""
        student = await self.session.execute(
            select(Student)
            .join(User)
            .where(Student.user_id == user_id, Student.is_verified == True)
            .options(joinedload(Student.user))
        )
        return student.scalar_one_or_none()

    @sqlalchemy_exceptions
    async def get_all_students(self) -> list[Student]:
        """Get all students"""
        students = await self.session.execute(
            select(Student)
            .join(User)
            .where(Student.is_verified == True)
            .options(joinedload(Student.user))
        )
        return students.scalars().all()

    @sqlalchemy_exceptions
    async def get_all_students_by_college(self, college_id: UUID) -> list[Student]:
        """Get all students by college"""
        students = await self.session.execute(
            select(Student)
            .join(User)
            .where(User.college_id == college_id, Student.is_verified == True)
            .options(joinedload(Student.user))
        )
        return students.scalars().all()

    @sqlalchemy_exceptions
    async def create_student(self, student: Student) -> Student:
        """Create a new student"""
        self.session.add(student)
        await self.session.commit()
        await self.session.refresh(student)
        return student

    @sqlalchemy_exceptions
    async def update_student(self, student: Student) -> Student:
        """Update a student"""
        await self.session.flush()
        await self.session.refresh(student)
        return student

    @sqlalchemy_exceptions
    async def delete_student(self, student_id: UUID) -> None:
        """Delete a student"""
        await self.session.execute(delete(Student).where(Student.id == student_id))
        await self.session.commit()


def get_student_repository(
    db: AsyncSession = Depends(get_async_session),
) -> StudentRepository:
    return StudentRepository(db)
