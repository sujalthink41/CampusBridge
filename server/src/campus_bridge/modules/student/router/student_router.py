from uuid import UUID

from campus_bridge.data.enums.role import RoleEnum
from fastapi import APIRouter, Depends, status

from campus_bridge.data.models import User
from campus_bridge.api.v1.dependencies import get_current_user
from campus_bridge.data.schemas.student import StudentUserResponse, StudentResponse, StudentUpdateRequest, StudentCreate, StudentUpdateResponse
from campus_bridge.modules.student.service.student_service import StudentService, get_student_service
from campus_bridge.errors.exc import UnauthorizedError

router = APIRouter(prefix="/student", tags=["student"])

@router.get("/me", status_code=status.HTTP_200_OK, response_model=StudentUserResponse)
async def get_current_student(
    current_user: User = Depends(get_current_user),
    student_service: StudentService = Depends(get_student_service)
):
    """Get current student details""" 
    return await student_service.get_current_student(current_user)

@router.get("/", status_code=status.HTTP_200_OK, response_model=list[StudentUserResponse])
async def get_all_students(
    current_user: User = Depends(get_current_user),
    student_service: StudentService = Depends(get_student_service)
):
    """Get all students"""
    if current_user.role != RoleEnum.ADMIN:
        raise UnauthorizedError(
            obj="student",
            act="get_all_students"
        )
    return await student_service.get_all_students(current_user)

@router.get("/college", status_code=status.HTTP_200_OK, response_model=list[StudentUserResponse])
async def get_all_students_by_college(
    current_user: User = Depends(get_current_user),
    student_service: StudentService = Depends(get_student_service)
):
    """Get all students of current user college"""
    return await student_service.get_all_students_by_college(current_user.college_id)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=StudentResponse)
async def create_student(
    student: StudentCreate,
    current_user: User = Depends(get_current_user),
    student_service: StudentService = Depends(get_student_service)
):
    """Create a new Student"""
    if current_user.role != RoleEnum.ADMIN or current_user.role != RoleEnum.STUDENT or current_user.role != RoleEnum.OFFICIALS:
        raise UnauthorizedError(
            obj="student",
            act="create"
        )   
    return await student_service.create_student(student, current_user)

@router.patch("/", status_code=status.HTTP_200_OK, response_model=StudentUpdateResponse)
async def update_student(
    student: StudentUpdateRequest,
    current_user: User = Depends(get_current_user),
    student_service: StudentService = Depends(get_student_service)
):
    """Partially update student details"""
    if current_user.role != RoleEnum.ADMIN or current_user.role != RoleEnum.STUDENT or current_user.role != RoleEnum.OFFICIALS:
        raise UnauthorizedError(
            obj="student",
            act="update"
        )
    return await student_service.update_student(student, current_user)

@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_student(
    current_user: User = Depends(get_current_user),
    student_service: StudentService = Depends(get_student_service)
):
    """Delete student profile"""
    if current_user.role != RoleEnum.ADMIN or current_user.role != RoleEnum.OFFICIALS:
        raise UnauthorizedError(
            obj="student",
            act="delete"
        )
    return await student_service.delete_student(current_user)
