import structlog
from fastapi import status, Depends

from campus_bridge.config.settings.app import app_settings
from campus_bridge.core.security import hash_password, verify_password, create_access_token
from campus_bridge.data.models.user import User
from campus_bridge.errors.exc import (
    AlreadyExistsError,
    InternalError,
    UnAuthenticatedError
)
from campus_bridge.data.schemas.auth import (
    RegisterRequest,
    LoginRequest,
    TokenResponse
)
from campus_bridge.modules.auth.repository.auth import (
    AuthRepository,
    get_auth_repository
)

logger = structlog.stdlib.get_logger(__name__)

class AuthService:
    def __init__(
        self,
        repository: AuthRepository,
    ):
        self.repository = repository

    async def register(
        self, 
        payload: RegisterRequest,
    ):
        """Register User"""
        existing_user = await self.repository.get_by_email(payload.email)
        if existing_user:
            logger.info(
                "User already exists with the current email",
                email=payload.email,
            )
            raise AlreadyExistsError("User", payload.email)

        try:
            user = User(
                college_id=payload.college_id,
                email=payload.email,
                password=hash_password(payload.password),
                phone=payload.phone,
                role=payload.role,
            )
            await self.repository.create(user)
        except Exception as exc:
            raise InternalError(
                details="Failed to create user",
                exc=exc,
            )

        logger.info("Auth Register Success", user_id=str(user.id))
        return str(user.id)
    
    async def login(
        self,
        payload: LoginRequest
    ):
        user = await self.repository.get_by_email(payload.email)
        if not user:
            logger.info("Auth login user not found", email=payload.email)
            raise UnAuthenticatedError(
                details="User not found",
                message="Invalid email or password",
            )

        if not verify_password(payload.password, user.password):
            logger.info("Auth login invalid password", user_id=str(user.id))
            raise UnAuthenticatedError(
                details="Invalid Password",
                message="Invalid email or password",
            )

        if not user.is_verified:
            logger.info("Auth login user not verified", user_id=str(user.id))
            raise UnAuthenticatedError(
                details="Email not verified",
                message="Email not verified"
            )

        try:
            token = create_access_token(
                subject=str(user.id),
                role=user.role.value,
                college_id=str(user.college_id)
            )
        except Exception as exc:
            raise InternalError(
                details="Failed to create access token",
                exc=exc
            )

        logger.info("Auth login Success", user_id=str(user.id))
        return TokenResponse(
            access_token=token,
            token_type="bearer",
        )


def get_auth_service(
    repository: AuthRepository = Depends(get_auth_repository)
) -> AuthService:
    return AuthService(repository)