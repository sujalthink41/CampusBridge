from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Depends, Query, status

from campus_bridge.api.v1.dependencies import get_current_user, require_admin
from campus_bridge.data.enums.role import RoleEnum
from campus_bridge.data.models.user import User
from campus_bridge.data.schemas.user import (
    UserResponse,
    UserUpdateRequest,
    UserUpdateResponse,
)
from campus_bridge.modules.users.service.user_service import (
    UserService,
    get_user_service,
)

router = APIRouter(prefix="/user", tags=["users"])


@router.get("/me", status_code=status.HTTP_200_OK, response_model=UserResponse)
async def get_current_user_profile(
    current_user: User = Depends(get_current_user),
) -> UserResponse:
    """Get the current authenticated user's profile"""
    return UserResponse.model_validate(current_user)


@router.get(
    "/college/{college_id}",
    status_code=status.HTTP_200_OK,
    response_model=list[UserResponse],
)
async def get_all_users_by_college_id_or_role(
    college_id: UUID | str,
    role: Optional[RoleEnum] = Query(
        None, description="Filter by role (STUDENT, ADMIN, ALUMNI, OFFICIALS)"
    ),
    admin_user: User = Depends(require_admin),
    user_service: UserService = Depends(get_user_service),
) -> list[UserResponse]:
    """Get all users in a college, optionally filtered by role. Admin only."""
    if admin_user:
        users = await user_service.get_all_users_by_college_id_or_role(
            college_id=college_id, role=role
        )
        return [UserResponse.model_validate(user) for user in users]


@router.patch(
    "/{user_id}", status_code=status.HTTP_200_OK, response_model=UserUpdateResponse
)
async def update_user(
    user_id: UUID,
    user_data: UserUpdateRequest,
    admin_user: User = Depends(require_admin),
    user_service: UserService = Depends(get_user_service),
) -> UserUpdateResponse:
    """Update a user's information. Admin only."""
    if admin_user:
        return await user_service.update_user(user_id, user_data)


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: UUID,
    admin_user: User = Depends(require_admin),
    user_service: UserService = Depends(get_user_service),
) -> None:
    """Soft delete a user. Admin only."""
    if admin_user:
        await user_service.delete_user(user_id)
