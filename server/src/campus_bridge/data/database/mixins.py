from tokenize import String
import uuid
from datetime import datetime
from typing import case 

from sqlalchemy import Boolean, DateTime, func 
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, declared_attr

from campus_bridge.utils.db_object import get_database_native_name

class IdMixin:
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

class TableNameMixin:
    @declared_attr.directive
    def __tablename__(cls) -> str:
        cls = case(type, cls)
        return get_database_native_name(cls.__name__, "table")

class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=func.now(),
        onupdate=func.now(),
        nullable=False
    )

class SoftDeleteMixin:
    is_deleted: Mapped[bool] = mapped_column(
        Boolean, 
        default=False,
        nullable=False
    )

class UserIdCard:
    id_card_url: Mapped[str] = mapped_column(
        String(500),
        nullable=False
    )

class VerifyAccount:
    is_verified: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False
    )