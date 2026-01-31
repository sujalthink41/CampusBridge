from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Depends, Query, status

from campus_bridge.api.v1.dependencies import get_current_user
from campus_bridge.data.enums.role import RoleEnum
from campus_bridge.data.models import User
from campus_bridge.data.schemas.alumni import (
    AlumniResponse,
    CreateAlumni,
    UpdateAlumni,
    UpdateAlumniResponse,
)
from campus_bridge.errors.exc import UnauthorizedError
from campus_bridge.modules.alumni.service.alumni_service import (
    AlumniService,
    get_alumni_service,
)

router = APIRouter(prefix="/alumni", tags=["Alumni"])


@router.get("/me", status_code=status.HTTP_200_OK, response_model=AlumniResponse)
async def get_current_alumni(
    current_user: User = Depends(get_current_user),
    alumni_service: AlumniService = Depends(get_alumni_service),
):
    """Get the the current aluni profile"""
    return await alumni_service.get_current_alumni(current_user)


@router.get("/", status_code=status.HTTP_200_OK, response_model=list[AlumniResponse])
async def get_all_alumni(
    current_user: User = Depends(get_current_user),
    alumni_service: AlumniService = Depends(get_alumni_service),
):
    """Get all alumni"""
    if current_user.role != RoleEnum.ADMIN:
        raise UnauthorizedError(obj="alumni", act="get_all_alumni_by_admin_only")
    return await alumni_service.get_all_alumni()


@router.get(
    "/college", status_code=status.HTTP_200_OK, response_model=list[AlumniResponse]
)
async def get_all_alumni_by_college(
    college_id: Optional[UUID] = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    current_user: User = Depends(get_current_user),
    alumni_service: AlumniService = Depends(get_alumni_service),
):
    """Get all alumni of current user college or a specified college (Admin only)"""

    # If Admin provides a college_id, they can see that specific college.
    if current_user.role == RoleEnum.ADMIN and college_id:
        target_college_id = college_id

    # If college_id is provided but the user is not an Admin, check BOLA.
    elif college_id and college_id != current_user.college_id:
        raise UnauthorizedError(obj="alumni", act="view_alumni_of_other_college")

    # Default to current user's college (for both non-admins and admins without college_id).
    else:
        target_college_id = current_user.college_id

    return await alumni_service.get_all_alumni_by_college(
        college_id=target_college_id, skip=skip, limit=limit
    )


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=AlumniResponse)
async def create_alumni(
    alumni: CreateAlumni,
    current_user: User = Depends(get_current_user),
    alumni_service: AlumniService = Depends(get_alumni_service),
):
    """Create a new alumni profile"""

    # Permission check: Allowed roles
    if current_user.role not in [RoleEnum.ADMIN, RoleEnum.OFFICIALS, RoleEnum.ALUMNI]:
        raise UnauthorizedError(obj="alumni", act="create_alumni")

    # Determine the target user (default to current user if not provided)
    target_user_id = alumni.user_id or current_user.id

    # 1. Admin: Full access (Can create for any college/user)
    if current_user.role == RoleEnum.ADMIN:
        pass

    # 2. Officials: Can only create alumni under their own college
    elif current_user.role == RoleEnum.OFFICIALS:
        if alumni.college_id and alumni.college_id != current_user.college_id:
            raise UnauthorizedError(obj="alumni", act="create_alumni_in_other_college")

    # 3. Alumni: Can only create their own profile under their own college
    elif current_user.role == RoleEnum.ALUMNI:
        if target_user_id != current_user.id:
            raise UnauthorizedError(
                obj="alumni", act="create_alumni_profile_for_another_user"
            )
        if alumni.college_id and alumni.college_id != current_user.college_id:
            raise UnauthorizedError(
                obj="alumni", act="create_alumni_profile_in_another_college"
            )

    return await alumni_service.create_alumni(alumni, target_user_id)


@router.patch("/", status_code=status.HTTP_200_OK, response_model=UpdateAlumniResponse)
async def update_alumni(
    alumni: UpdateAlumni,
    alumni_id: Optional[UUID] = Query(None),
    current_user: User = Depends(get_current_user),
    alumni_service: AlumniService = Depends(get_alumni_service),
):
    """Update of an alumni profile"""
    if current_user.role not in [RoleEnum.ADMIN, RoleEnum.OFFICIALS, RoleEnum.ALUMNI]:
        raise UnauthorizedError(
            obj="alumni", act="update_alumni_by_admin_officials_alumni_only"
        )
    # update alumni by id only for admin and officials
    if alumni_id and (
        current_user.role == RoleEnum.ADMIN or current_user.role == RoleEnum.OFFICIALS
    ):
        return await alumni_service.update_alumni(alumni, alumni_id)
    # update current user's alumni profile only for alumni
    return await alumni_service.update_alumni(alumni, current_user.id)


@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_alumni(
    alumni_id: Optional[UUID] = Query(None),
    current_user: User = Depends(get_current_user),
    alumni_service: AlumniService = Depends(get_alumni_service),
):
    """Delete an alumni profile"""
    if current_user.role not in [RoleEnum.ADMIN, RoleEnum.OFFICIALS, RoleEnum.ALUMNI]:
        raise UnauthorizedError(
            obj="alumni", act="delete_alumni_by_admin_officials_only"
        )

    if alumni_id and (
        current_user.role == RoleEnum.ADMIN or current_user.role == RoleEnum.OFFICIALS
    ):
        return await alumni_service.delete_alumni(alumni_id)
    return await alumni_service.delete_alumni(current_user.id)
