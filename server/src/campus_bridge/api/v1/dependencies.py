import structlog
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from campus_bridge.data.database.core import AsyncSessionLocal
from campus_bridge.core.security import verify_access_token
from campus_bridge.errors.exc import UnAuthenticatedError
from campus_bridge.modules.users.service.user_service import get_user_service, UserService

logger = structlog.stdlib.get_logger(__name__)
security = HTTPBearer()

async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception as exc:
            logger.exception("Database transaction failed", exc=exc)
            await session.rollback()
            raise

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    user_service: UserService = Depends(get_user_service)
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
            details="Missing sub key in the payload",
            message="Invalid access token"
        )
    
    # fetch user via service
    user = await user_service.get_user_by_id(user_id=user_id)
    return user


async def require_admin(
    current_user: User = Depends(get_current_user)
) -> User:
    """Dependency to ensure the current user is an admin"""
    from campus_bridge.data.enums.role import RoleEnum
    from campus_bridge.errors.exc import UnauthorizedError
    
    if current_user.role != RoleEnum.ADMIN:
        logger.warning("Non-admin user attempted admin action", user_id=str(current_user.id))
        raise UnauthorizedError(
            obj="admin resources",
            act="access"
        )
    
    return current_user
