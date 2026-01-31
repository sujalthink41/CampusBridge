from uuid import UUID

from fastapi import APIRouter, Depends, status

from campus_bridge.api.v1.dependencies import get_current_user
from campus_bridge.data.enums.role import RoleEnum
from campus_bridge.data.models.user import User
from campus_bridge.data.schemas.college import (
    CollegeDeleteResponse,
    CollegeResponse,
    CollegeUpdateRequest,
    CreateCollegeRequest,
)
from campus_bridge.errors.exc.base_errors import UnauthorizedError
from campus_bridge.modules.college.service.college_service import (
    CollegeService,
    get_college_service,
)

router = APIRouter(prefix="/college", tags=["college"])


@router.post(
    "", response_model=list[CollegeResponse], status_code=status.HTTP_201_CREATED
)
async def create_colleges(
    payload: list[CreateCollegeRequest],
    current_user: User = Depends(get_current_user),
    college_service: CollegeService = Depends(get_college_service),
):
    if current_user.role != RoleEnum.ADMIN:
        raise UnauthorizedError(obj="college", act="create")

    return await college_service.create_colleges(payload=payload)


@router.patch(
    "/{college_id}", response_model=CollegeResponse, status_code=status.HTTP_200_OK
)
async def update_college(
    college_id: UUID,
    payload: CollegeUpdateRequest,
    current_user: User = Depends(get_current_user),
    college_service: CollegeService = Depends(get_college_service),
):
    if current_user.role != RoleEnum.ADMIN:
        raise UnauthorizedError(obj="college", act="update")

    return await college_service.update_college(college_id=college_id, payload=payload)


@router.delete(
    "/{college_id}",
    response_model=CollegeDeleteResponse,
    status_code=status.HTTP_200_OK,
)
async def delete_college(
    college_id: UUID,
    current_user: User = Depends(get_current_user),
    college_service: CollegeService = Depends(get_college_service),
):
    if current_user.role != RoleEnum.ADMIN:
        raise UnauthorizedError(obj="college", act="delete")

    return await college_service.delete_college(college_id=college_id)


@router.get(
    "/{college_id}", response_model=CollegeResponse, status_code=status.HTTP_200_OK
)
async def get_college_by_id(
    college_id: UUID,
    current_user: User = Depends(get_current_user),
    college_service: CollegeService = Depends(get_college_service),
):
    if current_user.role != RoleEnum.ADMIN:
        raise UnauthorizedError(obj="college", act="get_single_college")

    return await college_service.get_college_by_id(college_id=college_id)


@router.get("", response_model=list[CollegeResponse], status_code=status.HTTP_200_OK)
async def get_all_college(
    current_user: User = Depends(get_current_user),
    college_service: CollegeService = Depends(get_college_service),
):
    if current_user.role != RoleEnum.ADMIN:
        raise UnauthorizedError(obj="college", act="get_all_college")

    return await college_service.get_all_college()
