import uuid

from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from campus_bridge.data.database.base import Base
from campus_bridge.data.database.mixins import IdMixin, TableNameMixin, TimestampMixin
from campus_bridge.data.enums.reaction import ReactionTypeEnum, reaction_type_enum
from campus_bridge.utils.db_object import get_foreign_key


class PostReaction(Base, IdMixin, TableNameMixin, TimestampMixin):
    post_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey(get_foreign_key("Post")), nullable=False
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey(get_foreign_key("User")), nullable=False
    )
    reaction: Mapped[ReactionTypeEnum] = mapped_column(
        reaction_type_enum, nullable=False
    )

    __table_args__ = (
        UniqueConstraint("post_id", "user_id", name="uq_post_user_reaction"),
    )

    # relationship
    post: Mapped["Post"] = relationship("Post", back_populates="reactions")
    user: Mapped["User"] = relationship("User")
