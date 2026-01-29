import structlog

from datetime import datetime 
from uuid import UUID

from sqlalchemy import and_, or_, desc
from sqlalchemy.sql import Select

from campus_bridge.errors.exc import BadRequestError

logger = structlog.stdlib.get_logger(__name__)

def cursor_pagination(
    stmt: Select, 
    *,
    cursor: str | None,
    limit: int,
    created_at_column,
    id_column,
) -> Select:
    """
    Apply cursor-based pagination to a SQLAlchemy Select query.
    
    Cursor format : Cursor is just a value.
    "<created_at_iso>|<uuid>"

    Example:
    "2026-01-29T10:30:22.123456+00:00|550e8400-e29b-41d4-a716-446655440000"
    """

    if cursor:
        try:
            cursor_created_at_str, cursor_id_str = cursor.split("|")
            logger.info("cursor_values", extra={"created_at": cursor_created_at_str, "id": cursor_id_str})
            cursor_created_at = datetime.fromisoformat(cursor_created_at_str)
            cursor_id = UUID(cursor_id_str)
        except ValueError as e:
            logger.warning("invalid_cursor_format", cursor=cursor)  
            raise BadRequestError(
                message="Invalid cursor format",
                details=f"Invalid cursor format: {cursor}",
            )    
        
        stmt = stmt.where(
            or_(
                created_at_column < cursor_created_at,
                and_(
                    created_at_column == cursor_created_at,
                    id_column < cursor_id,
                ),
            )
        )

    return (
        stmt
        .order_by(desc(created_at_column), desc(id_column))
        .limit(limit)
    )