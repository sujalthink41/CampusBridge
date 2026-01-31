from uuid import UUID

import structlog
from fastapi import Depends

from campus_bridge.data.models.student import Student
from campus_bridge.data.models.user import User
from campus_bridge.data.schemas.student import (
    StudentCreate,
    StudentResponse,
    StudentUpdateRequest,
    StudentUpdateResponse,
    StudentUserResponse,
)
from campus_bridge.errors.exc import ConflictError, NotFoundError
from campus_bridge.modules.student.repository.student_repository import (
    StudentRepository,
    get_student_repository,
)

logger = structlog.get_logger(__name__)


class StudentService:
    def __init__(self, student_repository: StudentRepository):
        self.student_repository = student_repository

    async def get_current_student(self, user: User) -> StudentUserResponse:
        """Get a current student profile"""

        student = await self.student_repository.get_by_user_id(user.id)
        if not student:
            logger.error("Student not found", user_id=str(user.id))
            raise NotFoundError(resource="Student", message="Student not found")
        logger.info("Student found", user_id=str(user.id), student_id=str(student.id))
        return StudentUserResponse(student=student, user=user)

    async def get_all_students(self, user: User) -> list[StudentUserResponse]:
        """Get all students"""

        students = await self.student_repository.get_all_students()
        if not students:
            logger.error("Students not found", user_id=str(user.id))
            raise NotFoundError(resource="Students", message="Students not found")
        logger.info(
            "Students found", user_id=str(user.id), students_count=len(students)
        )
        return [
            StudentUserResponse(student=student, user=student.user)
            for student in students
        ]

    async def get_all_students_by_college(
        self, college_id: UUID
    ) -> list[StudentUserResponse]:
        """Get all students by college"""

        students = await self.student_repository.get_all_students_by_college(college_id)
        if not students:
            logger.error("Students not found", college_id=str(college_id))
            raise NotFoundError(resource="Students", message="Students not found")
        logger.info(
            "Students found", college_id=str(college_id), students_count=len(students)
        )
        return [
            StudentUserResponse(student=student, user=student.user)
            for student in students
        ]

    async def create_student(
        self, student: StudentCreate, user: User
    ) -> StudentResponse:
        """Create a new Student"""

        # check if student already exists with the current user id
        existing_student = await self.student_repository.get_by_user_id(user.id)
        if existing_student:
            logger.error("Student already exists", user_id=str(user.id))
            raise ConflictError(resource="Student", message="Student already exists")

        # create student
        student = Student(
            user_id=user.id,
            first_name=student.first_name,
            middle_name=student.middle_name,
            last_name=student.last_name,
            roll_number=student.roll_number,
            branch=student.branch,
            year_of_study=student.year_of_study,
            interests=student.interests,
        )

        student = await self.student_repository.create_student(student)
        logger.info("Student created", user_id=str(user.id), student_id=str(student.id))
        return StudentResponse.model_validate(student)

    async def update_student(
        self, student: StudentUpdateRequest, user: User
    ) -> StudentUpdateResponse:
        """Update student profile (partially)"""

        # check if the current user is a student
        student = await self.student_repository.get_by_user_id(user.id)
        if not student:
            logger.error("Student not found", user_id=str(user.id))
            raise NotFoundError(resource="Student", message="Student not found")
        logger.info("Student found", user_id=str(user.id), student_id=str(student.id))

        for field, value in student.model_dump(exclude_unset=True).items():
            setattr(student, field, value)

        updated_student = await self.student_repository.update_student(student)
        logger.info(
            "Student updated",
            user_id=str(user.id),
            student_id=str(student.id),
            updated_fields=list(updated_student.keys()),
        )
        return StudentUpdateResponse.model_validate(updated_student)

    async def delete_student(self, user: User) -> None:
        """Delete student profile"""

        # check if the current user is a student
        student = await self.student_repository.get_by_user_id(user.id)
        if not student:
            logger.error("Student not found", user_id=str(user.id))
            raise NotFoundError(resource="Student", message="Student not found")
        logger.info("Student found", user_id=str(user.id), student_id=str(student.id))

        await self.student_repository.delete_student(student.id)
        logger.info("Student deleted", user_id=str(user.id), student_id=str(student.id))


def get_student_service(
    student_repository: StudentRepository = Depends(get_student_repository),
) -> StudentService:
    return StudentService(student_repository)
