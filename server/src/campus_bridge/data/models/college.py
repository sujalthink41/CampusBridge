from campus_bridge.data.enums.state import StateEnum, state_enum
from sqlalchemy import String, Boolean, UniqueConstraint
from sqlalchemy.orm import mapped_column, Mapped, relationship

from campus_bridge.data.database.base import Base
from campus_bridge.data.database.mixins import (
    IdMixin,
    SoftDeleteMixin,
    TableNameMixin,
    TimestampMixin
)

class College(
    Base, 
    IdMixin,
    TableNameMixin,
    TimestampMixin,
    SoftDeleteMixin
):
    __table_args__ = (
        UniqueConstraint("name", "city", "state", name="uq_college_identity"),
    )

    name: Mapped[str] = mapped_column(
        String(250), 
        nullable=False,
        index=True
    )
    is_government: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False
    )
    state: Mapped[StateEnum] = mapped_column(
        state_enum,
        nullable=False,
        index=True
    )
    city: Mapped[str] = mapped_column(
        String(100), 
        nullable=False,
        index=True
    )

    posts: Mapped[list["Post"]] = relationship(
        "Post",
        back_populates="college"
    )   