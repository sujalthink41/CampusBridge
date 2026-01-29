import uuid 

from campus_bridge.utils.db_object import get_foreign_key
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from campus_bridge.data.database.base import Base
from campus_bridge.data.database.mixins import (
    IdMixin,
    TableNameMixin,
    TimestampMixin,
    UserIdCard,
    VerifyAccount
)

class CollegeOfficial(
    Base,
    IdMixin,
    TableNameMixin,
    TimestampMixin,
    UserIdCard,
    VerifyAccount
):

    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey(get_foreign_key("User")),
        nullable=False,
        unique=True,
        index=True
    )
    department: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    # relationship 
    user: Mapped["User"] = relationship(
        "User",
        back_populates="official_profile"
    )