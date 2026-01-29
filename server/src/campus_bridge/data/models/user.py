import uuid 

from campus_bridge.data.enums.role import RoleEnum, role_enum
from campus_bridge.data.models.alumni import Alumni
from campus_bridge.data.models.college_official import CollegeOfficial
from campus_bridge.data.models.student import Student
from campus_bridge.utils.db_object import get_foreign_key
from sqlalchemy import ForeignKey, String, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

from campus_bridge.data.database.base import Base
from campus_bridge.data.database.mixins import (
    IdMixin,
    SoftDeleteMixin,
    TableNameMixin,
    TimestampMixin,
    VerifyAccount
)

class User(
    Base, 
    IdMixin,
    TableNameMixin,
    TimestampMixin,
    SoftDeleteMixin,
    VerifyAccount
):
    college_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey(get_foreign_key("College")),
        nullable=False
    )
    email: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        unique=True
    )
    password: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )
    phone: Mapped[str] = mapped_column(
        String(15),
        nullable=False,
        unique=True
    )
    role: Mapped[RoleEnum] = mapped_column(
        role_enum,
        nullable=False,
        index=True
    )

     # relationships
    student_profile: Mapped["Student"] = relationship(
        "Student",
        back_populates="user",
        uselist=False
    )

    alumni_profile: Mapped["Alumni"] = relationship(
        "Alumni",
        back_populates="user",
        uselist=False
    )

    official_profile: Mapped["CollegeOfficial"] = relationship(
        "CollegeOfficial",
        back_populates="user",
        uselist=False
    )
    posts: Mapped[list["Post"]] = relationship(
        "Post",
        back_populates="user",
        cascade="all, delete-orphan"
    )
    email_verifications: Mapped[list["EmailVerification"]] = relationship(
        "EmailVerification",
        back_populates="user",
        cascade="all, delete-orphan"
    )
