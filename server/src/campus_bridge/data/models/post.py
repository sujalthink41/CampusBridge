import uuid 

from sqlalchemy import ForeignKey, String, Text, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import JSONB

from campus_bridge.data.database.base import Base
from campus_bridge.utils.db_object import get_foreign_key
from campus_bridge.data.models.user import User
from campus_bridge.data.enums.post import (
    PostTypeEnum,
    post_type_enum,
    PostVisibilityEnum,
    post_visibility_type_enum
)
from campus_bridge.data.database.mixins import (
    IdMixin,
    TableNameMixin,
    TimestampMixin,
    SoftDeleteMixin
)

class Post(
    Base,
    IdMixin,
    TableNameMixin,
    TimestampMixin,
    SoftDeleteMixin
):

    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey(get_foreign_key("User")),
        nullable=False,
        index=True
    )
    college_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey(get_foreign_key("College")),
        nullable=False,
        index=True
    )   
    content: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )
    post_type: Mapped[PostTypeEnum] = mapped_column(
        post_type_enum,
        default=PostTypeEnum.TEXT,
        nullable=False,
    )
    visibility: Mapped[PostVisibilityEnum] = mapped_column(
        post_visibility_type_enum,
        default=PostVisibilityEnum.PUBLIC,
        nullable=False
    )
    is_hidden: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False
    )
    meta_data: Mapped[dict] = mapped_column(
        JSONB,
        nullable=True,
        default=dict
    )

    # relationship
    user: Mapped["User"] = relationship(
        "User",
        back_populates="posts"
    )
    comments: Mapped["Comment"] = relationship(
        "Comment",
        back_populates="post",
        cascade="all, delete-orphan"
    )
    reactions: Mapped[list["PostReaction"]] = relationship(
        "PostReaction",
        back_populates="post",
        cascade="all, delete-orphan"
    )
    college: Mapped["College"] = relationship(
        "College",
        back_populates="posts"
    )   