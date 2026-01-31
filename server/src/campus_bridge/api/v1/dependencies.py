import structlog
from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from campus_bridge.core.security import verify_access_token
from campus_bridge.data.database.session import get_async_session
from campus_bridge.data.enums.role import RoleEnum
from campus_bridge.data.models.user import User
from campus_bridge.errors.exc import UnAuthenticatedError, UnauthorizedError
from campus_bridge.modules.users.service.user_service import (
    UserService,
    get_user_service,
)

logger = structlog.stdlib.get_logger(__name__)
security = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    user_service: UserService = Depends(get_user_service),
):
    """Dependencies to get the current authenticated user"""
    logger.debug("Resolving current user from token")
    token = credentials.credentials

    # now verify jwt
    payload = verify_access_token(token=token)

    # now extract user id
    user_id = payload.get("sub")
    if not user_id:
        logger.warning("Missing sub in JWT payload")
        raise UnAuthenticatedError(
            details="Missing sub key in the payload", message="Invalid access token"
        )

    # fetch user via service
    user = await user_service.get_user_by_id(user_id=user_id)
    return user


async def require_admin(current_user: User = Depends(get_current_user)) -> User:
    """Dependency to ensure the current user is an admin"""
    if current_user.role != RoleEnum.ADMIN:
        logger.warning(
            "Non-admin user attempted admin action", user_id=str(current_user.id)
        )
        raise UnauthorizedError(obj="admin resources", act="access")

    return current_user


async def require_admin_or_officials_or_alumni(
    current_user: User = Depends(get_current_user),
) -> User:
    """Dependency to ensume the current is an admin or officials or alumni"""
    if current_user.role not in [RoleEnum.ADMIN, RoleEnum.OFFICIALS, RoleEnum.ALUMNI]:
        logger.warning(
            "Non-admin or officials or alumni user attempted admin or officials or alumni action",
            user_id=str(current_user.id),
        )
        raise UnauthorizedError(
            obj="admin or officials or alumni resources", act="access"
        )

    return current_user
