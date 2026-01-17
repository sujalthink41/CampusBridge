from typing import Optional
from uuid import UUID

def parse_uuid(value: str | None) -> Optional[UUID]:
    if not value:
        return None
    try:
        return UUID(value)
    except (ValueError, AttributeError, TypeError):
        return None
