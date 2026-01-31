from typing import Optional
from uuid import UUID

import structlog
from fastapi import Depends

from campus_bridge.data.enums.role import RoleEnum
from campus_bridge.data.models.user import User
from campus_bridge.data.schemas.user import UserUpdateRequest, UserUpdateResponse
from campus_bridge.errors.exc import BadRequestError, UnAuthenticatedError
from campus_bridge.modules.users.repository.user_repository import (
    UserRepository,
    get_user_repository,
)
from campus_bridge.utils.uuid import parse_uuid

logger = structlog.stdlib.get_logger(__name__)


class UserService:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    async def get_user_by_id(self, user_id: str | UUID) -> User:
        """Get user by id"""
        user_id = user_id if isinstance(user_id, UUID) else parse_uuid(user_id)
        if user_id is None:
            logger.warning("Invalid user_id format")
            raise BadRequestError(
                message="Invalid user ID format",
                details="The provided user ID is not a valid UUID",
            )

        user = await self.repository.get_user_by_id(user_id=user_id)
        if user is None:
            logger.warning("User not found", user_id=str(user_id))
            raise UnAuthenticatedError(
                details="User not found", message="User does not exist"
            )

        logger.debug("User resolved", user_id=str(user.id))
        return user

    async def get_all_users_by_college_id_or_role(
        self, college_id: str | UUID, role: Optional[RoleEnum] = None
    ) -> list[User]:
        """Get all users by college id, optionally filtered by role"""
        college_id = (
            college_id if isinstance(college_id, UUID) else parse_uuid(college_id)
        )

        if college_id is None:
            logger.warning("Invalid college_id provided")
            raise BadRequestError(
                message="Invalid college ID format",
                details="The provided college ID is not a valid UUID",
            )

        logger.info(
            "Fetching users by college",
            college_id=str(college_id),
            role=role.value if role else None,
        )
        users = await self.repository.get_all_users_by_college_id_or_role(
            college_id=college_id, role=role
        )
        logger.info("Users fetched successfully", count=len(users))

        return users

    async def update_user(
        self, user_id: UUID, user_data: UserUpdateRequest
    ) -> UserUpdateResponse:
        """Update a single user"""
        # Verify user exists
        await self.get_user_by_id(user_id=user_id)

        updated_data = user_data.model_dump(exclude_unset=True)
        if not updated_data:
            logger.warning("No data to update", user_id=str(user_id))
            raise BadRequestError(
                message="No data to update",
                details="At least one field must be provided for update",
            )

        logger.info(
            "Updating user", user_id=str(user_id), fields=list(updated_data.keys())
        )
        updated_user = await self.repository.update_user(
            user_id=user_id, updated_data=updated_data
        )
        logger.info("User updated successfully", user_id=str(user_id))
        return UserUpdateResponse.model_validate(updated_user)

    async def delete_user(self, user_id: UUID | str) -> None:
        """Soft Delete User"""
        # Verify user exists before deletion
        user = await self.get_user_by_id(user_id=user_id)

        logger.info("Deleting user", user_id=str(user.id))
        await self.repository.delete_user(user_id=user.id)
        logger.info("User deleted successfully", user_id=str(user.id))


def get_user_service(
    repository: UserRepository = Depends(get_user_repository),
) -> UserService:
    return UserService(repository)
