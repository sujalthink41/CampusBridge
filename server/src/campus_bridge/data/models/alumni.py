import uuid 

from campus_bridge.data.models.user import User
from campus_bridge.utils.db_object import get_foreign_key
from sqlalchemy import String, Integer, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import JSONB

from campus_bridge.data.database.base import Base
from campus_bridge.data.database.mixins import (
    TableNameMixin,
    TimestampMixin,
    IdMixin,
    UserIdCard,
    VerifyAccount
)

class Alumni(
    Base,
    IdMixin,
    TableNameMixin,
    TimestampMixin,
    UserIdCard,
    VerifyAccount
):
    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey(get_foreign_key("User"), nullable=False, unique=True, index=True)
    )
    graduation_year: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )
    company: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )
    designation: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )
    experience_years: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )
    expertise_areas: Mapped[dict] = mapped_column(
        JSONB,
        nullable=False,
        default=dict
    )
    is_available: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )

    #realtionship
    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey(get_foreign_key("User")),
        nullable=False,
        unique=True,
        index=True
    )