from uuid import UUID
from typing import Optional
from fastapi import APIRouter, status, Depends, Query

from campus_bridge.data.models.user import User
from campus_bridge.api.v1.dependencies import get_current_user
from campus_bridge.data.schemas.user import UserResponse, UserUpdateRequest, UserUpdateResponse
from campus_bridge.data.enums.role import RoleEnum
from campus_bridge.modules.users.service.user_service import UserService, get_user_service
from campus_bridge.errors.exc.base_errors import UnauthorizedError 

router = APIRouter(prefix="/user", tags=["users"])

@router.get("/me", status_code=status.HTTP_200_OK, response_model=UserResponse)
async def get_user(
    current_user: User = Depends(get_current_user)
): 
    return current_user

@router.get("/college/{college_id}", status_code=status.HTTP_200_OK, response_model=list[UserResponse])
async def get_all_users_by_college_id_or_role(
    college_id: UUID | str,
    role: Optional[RoleEnum] = Query(None, description="Filter by role (STUDENT, ADMIN, ALUMNI, OFFICIALS)"),
    current_user: User = Depends(get_current_user),
    user_service: UserService = Depends(get_user_service)
):
    if current_user.role != RoleEnum.ADMIN:
        raise UnauthorizedError(
            obj="users",
            act="view all users"
        )
    
    return await user_service.get_all_users_by_college_id_or_role(college_id=college_id, role=role)

@router.patch("/{user_id}", status_code=status.HTTP_200_OK, response_model=UserUpdateResponse)
async def update_user(
    user_id: UUID,
    user_data: UserUpdateRequest,
    current_user: User = Depends(get_current_user),
    user_service: UserService = Depends(get_user_service)
):
    if current_user.role != RoleEnum.ADMIN:
        raise UnauthorizedError(
            obj="users",
            act="update user"
        )
    
    return await user_service.update_user(user_id, user_data)

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: UUID,
    current_user: User = Depends(get_current_user),
    user_service: UserService = Depends(get_user_service)
):
    if current_user.role != RoleEnum.ADMIN:
        raise UnauthorizedError(
            obj="users",
            act="delete user"
        )

    return await user_service.delete_user(user_id)
    