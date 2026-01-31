import uuid

from sqlalchemy import ForeignKey, String
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from campus_bridge.data.enums.branch import BranchEnum, branch_enum
from campus_bridge.utils.db_object import get_foreign_key
from campus_bridge.data.database.mixins import (
    TableNameMixin,
    TimestampMixin,
    IdMixin,
    UserIdCard,
    VerifyAccount
)
from campus_bridge.data.database.base import Base

class Student(
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
    first_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )
    middle_name: Mapped[str] = mapped_column(
        String(100),
        nullable=True,
    )
    last_name: Mapped[str] = mapped_column(
        String(100),
        nullable=True
    )
    roll_number: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        index=True
    )
    branch: Mapped[BranchEnum] = mapped_column(
        branch_enum,
        nullable=False  
    )
    year_of_study: Mapped[int] = mapped_column(
        nullable=False
    )
    interests: Mapped[dict] = mapped_column(
        JSONB,
        nullable=False,
        default=dict
    ) 

    #relationship
    user: Mapped["User"] = relationship(
        "User",
        back_populates="student_profile",
        uselist=False
    )
    