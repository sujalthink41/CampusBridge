from typing import Any, Literal
from uuid import UUID

import structlog
from fastapi import HTTPException, status

# Type for log levels 
LogLevel = Literal["debug", "info", "warning", "error", "critical"]

class BaseError(HTTPException):
    def __init__(
        self,
        status_code: int,
        message: str,
        log_config: tuple[LogLevel, str, *tuple[Any, ...]] | None = None,
    ):
        super().__init__(status_code=status_code, detail=message)
        self.log_config = log_config

        self._log_error()

    def _log_error(self) -> None:
        if not self.log_config or len(self.log_config) < 2:
            return
        
        struct_logger = structlog.stdlib.get_logger(__name__)
        log_level = self.log_config[0]

        struct_log_method = getattr(struct_logger, log_level, struct_logger.error)

        # convert logs args to structured format 
        event_data = {
            "error_type": type(self).__name__,
            "status_code": self.status_code,
            "message": self.detail
        }
        
        if len(self.log_config) > 2:
            log_format = self.log_config[1]
            log_args = self.log_config[2:]
            event_data["details"] = log_format % log_args if log_args else log_format

        struct_log_method("error_raised", **event_data)


class NotFoundError(BaseError):
    def __init__(self, resource: str, identifier: str | int | UUID):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            message=f"{resource} with identifier '{identifier}' not found",
            log_config=(
                "warning",
                "%s not found with identifier: %s",
                resource,
                str(identifier)
            )
        )

class AlreadyExistsError(BaseError):
    def __init__(self, resource: str, identifier: str | int | UUID):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            message=f"{resource} with identifier '{identifier}' already exists.",
            log_config=(
                "warning",
                "%s already exists with identifier: %s",
                resource,
                str(identifier)
            )
        )

# TODO:(Sujal) -> wrap obj, act and owner in one schema later by name AuthorizedPolicyRequest
class UnauthorizedError(BaseError):
    def __init__(self, obj: str, act: str):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            message=f"You are not authorized to perform {act} action on {obj} resource",
            log_config=(
                "info",
                "unauthorized error: %s %s",
                obj,
                act
            )
        )

class BadRequestError(BaseError):
    def __init__(
        self, message: str, exc: Exception | None = None, details: str | None = None
    ):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            message=message,
            log_config=(
                "warning",
                "bad request: %s",
                message,
            ),
        )

class ConflictError(BaseError):
    def __init__(self, message: str):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            message=message,
            log_config=(
                "warning",
                "conflict: %s",
                message,
            ),
        )

class UnAuthenticatedError(BaseError):
    def __init__(
        self, details: str, exc: Exception | None = None, message: str | None = None
    ):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            message=message or "user not authorized",
            log_config=(
                "error",
                "user_unauthorized - %s: %s",
                details,
                str(exc),
            ),
        )

class InternalError(BaseError):
    def __init__(self, details: str, exc: Exception, message: str | None = None):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            message=message or "Something went wrong!",
            log_config=(
                "error",
                "Internal error - %s: %s",
                details,
                str(exc),
            ),
        )