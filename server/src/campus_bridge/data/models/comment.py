import uuid

from sqlalchemy import ForeignKey, Text, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

from campus_bridge.data.database.base import Base
from campus_bridge.utils.db_object import get_foreign_key
from campus_bridge.data.database.mixins import (
    IdMixin,
    TableNameMixin,
    TimestampMixin,
    SoftDeleteMixin
)

class Comment(
    Base,
    IdMixin,
    TableNameMixin,
    TimestampMixin,
    SoftDeleteMixin
):
    post_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey(get_foreign_key("Post")),
        nullable=False,
        index=True
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey(get_foreign_key("User")),
        nullable=False,
        index=True
    )
    parent_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey(get_foreign_key("Comment")),
        nullable=True,
        index=True
    )
    content: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )
    is_hidden: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False
    )

    # relationships
    user: Mapped["User"] = relationship("User")
    post: Mapped["Post"] = relationship("Post")
    parent = relationship(
        "Comment",
        remote_side="Comment.id",
        back_populates="replies"
    )
    replies = relationship(
        "Comment",
        back_populates="parent",
        cascade="all, delete-orphan"
    )
