from functools import wraps
from typing import Awaitable, Callable, TypeVar

import structlog
from sqlalchemy.exc import (
    DataError,
    IntegrityError,
    OperationalError,
    ProgrammingError,
    SQLAlchemyError,
)

from campus_bridge.errors.exc.base_errors import InternalError

logger = structlog.stdlib.get_logger(__name__)

T = TypeVar("T")


# TODO(Sujal): Join the logger within the Internal Error
def sqlalchemy_exceptions(
    func: Callable[..., Awaitable[T]],
) -> Callable[..., Awaitable[T]]:
    @wraps(func)
    async def wrapper(*args, **kwargs) -> T:
        try:
            return await func(*args, **kwargs)
        except IntegrityError as e:
            # Foreign key, unique constraint, not null violations, etc.
            logger.error(
                "Database integrity error",
                function=func.__name__,
                error_type=type(e).__name__,
                error_detail=str(e.orig) if hasattr(e, "orig") else str(e),
                statement=e.statement if hasattr(e, "statement") else None,
                params=e.params if hasattr(e, "params") else None,
            )

            raise InternalError(
                details=f"Database integrity error in {func.__name__}",
                exc=e,
                message="Something went wrong!",
            )
        except DataError as e:
            # Invalid data type, value out of range, etc.
            logger.error(
                "Database data error",
                function=func.__name__,
                error_type=type(e).__name__,
                error_detail=str(e.orig) if hasattr(e, "orig") else str(e),
                statement=e.statement if hasattr(e, "statement") else None,
            )
            raise InternalError(
                details=f"Database data error in {func.__name__}",
                exc=e,
                message="Something went wrong!",
            )
        except OperationalError as e:
            # Database connection issues, table doesn't exist, etc.
            logger.error(
                "Database operational error",
                function=func.__name__,
                error_type=type(e).__name__,
                error_detail=str(e.orig) if hasattr(e, "orig") else str(e),
            )
            raise InternalError(
                details=f"Database operational error in {func.__name__}",
                exc=e,
                message="Something went wrong!",
            )
        except ProgrammingError as e:
            # SQL syntax error, table/column doesn't exist, etc.
            logger.error(
                "Database programming error",
                function=func.__name__,
                error_type=type(e).__name__,
                error_detail=str(e.orig) if hasattr(e, "orig") else str(e),
                statement=e.statement if hasattr(e, "statement") else None,
            )
            raise InternalError(
                details=f"Database programming error in {func.__name__}",
                exc=e,
                message="Something went wrong!",
            )
        except SQLAlchemyError as e:
            # Catch-all for other SQLAlchemy errors
            logger.error(
                "Database error",
                function=func.__name__,
                error_type=type(e).__name__,
                error_detail=str(e),
            )
            raise InternalError(
                details=f"Database error in {func.__name__}",
                exc=e,
                message="Something went wrong!",
            )

    return wrapper
