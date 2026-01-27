import structlog
from uuid import UUID
from typing import Optional
from fastapi import Depends

from campus_bridge.data.models.user import User
from campus_bridge.data.schemas.user import UserUpdateRequest, UserUpdateResponse
from campus_bridge.errors.exc import UnAuthenticatedError, BadRequestError
from campus_bridge.data.enums.role import RoleEnum
from campus_bridge.modules.users.repository.user_repository import (
    UserRepository,
    get_user_repository
)
from campus_bridge.utils.uuid import parse_uuid

logger = structlog.stdlib.get_logger(__name__)

class UserService:
    def __init__(
        self, 
        repository: UserRepository
    ):
        self.repository = repository

    async def get_user_by_id(self, user_id: str | UUID) -> User:
        """Get current user from id"""
        user_id = user_id if isinstance(user_id, UUID) else parse_uuid(user_id)
        if user_id is None:
            logger.warning("Invalid user_id in token")
            raise UnAuthenticatedError(
            details="malformed_jwt_token",
            message="Invalid Token",
        )

        user = await self.repository.get_user_by_id(user_id=user_id)
        if user is None:
            logger.warning("User not found", user_id=str(user_id))
            raise UnAuthenticatedError(
                details="User not found",
                message="User does not exits"
            )

        logger.info("Current user resolved", user_id=str(user.id))
        return user

    async def get_all_users_by_college_id_or_role(self, college_id: str | UUID, role: Optional[RoleEnum] = None) -> list[User]:
        """Get all users by college id, optionally filtered by role"""
        college_id = college_id if isinstance(college_id, UUID) else parse_uuid(college_id)
        
        logger.info("Fetching users by college", college_id=str(college_id), role=role)
        users = await self.repository.get_all_users_by_college_id_or_role(college_id=college_id, role=role)
        logger.info("Users fetched successfully", count=len(users))
        
        return users

    async def update_user(self, user_id: UUID, user_data: UserUpdateRequest) -> UserUpdateResponse:
        """Update a single user"""
        await self.get_user_by_id(user_id=user_id)
        updated_data = user_data.model_dump(exclude_unset=True)
        if not updated_data: 
            logger.warning("No data to update")
            raise BadRequestError(
                message="No_data_to_update",
                details="There is no data to update"
            )
        updated_user = await self.repository.update_user(user_id=user_id,
        updated_data=updated_data)
        return UserUpdateResponse.model_validate(updated_user)

    async def delete_user(self, user_id: UUID | str):
        """Soft Delete User"""
        await self.get_user_by_id(user_id=user_id)
        await self.repository.delete_user(user_id=user_id)

def get_user_service(
    repository: UserRepository = Depends(get_user_repository)
) -> UserService:
    return UserService(repository)