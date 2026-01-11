from campus_bridge.data.enums.state import StateEnum, state_enum
from sqlalchemy import String, Boolean
from sqlalchemy.orm import mapped_column, Mapped

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
    name: Mapped[str] = mapped_column(
        String(250), 
        nullable=False
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