import uuid 
from datetime import datetime, timedelta

from sqlalchemy import Boolean, DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from campus_bridge.data.database.base import Base
from campus_bridge.data.database.mixins import (
    IdMixin,
    TableNameMixin,
    TimestampMixin
)
from campus_bridge.utils.db_object import get_foreign_key

class EmailVerification(
    Base, 
    IdMixin,
    TableNameMixin,
    TimestampMixin
):
    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey(get_foreign_key('User')),
        nullable=False,
        index=True 
    )
    otp_hash: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )
    expires_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False
    )
    is_used: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False
    )

    # relationship
    user: Mapped['User'] = relationship('User', back_populates="email_verifications")
    