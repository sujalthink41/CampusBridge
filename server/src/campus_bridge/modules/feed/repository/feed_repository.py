from uuid import UUID

from sqlalchemy import select, desc
from sqlalchemy.orm import joinedload 
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends

from campus_bridge.data.models.post import Post
from campus_bridge.data.enums.post import PostVisibilityEnum
from campus_bridge.data.database.session import get_async_session
from campus_bridge.errors.decorators.sqlalchemy import sqlalchemy_exceptions
from campus_bridge.utils.cursor_pagination import cursor_pagination

class FeedRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    @sqlalchemy_exceptions
    async def get_my_posts(self, user_id: UUID) -> list[Post]:
        """Get all posts of the current user"""
        stmt = (
            select(
                Post 
            ).where(
                Post.user_id == user_id,
                Post.is_hidden.is_(False),
            ).order_by(desc(Post.created_at))
            .options(joinedload(Post.user))
        )

        result = await self.db.execute(stmt)
        return result.scalars().all()

    @sqlalchemy_exceptions
    async def create_post(self, post: Post) -> Post:
        """Create User Post"""
        self.db.add(post)
        await self.db.flush()
        await self.db.refresh(post)
        return post 

    @sqlalchemy_exceptions
    async def get_college_posts(self, college_id: UUID, limit: int, cursor: str | None) -> list[Post]:
        """Get all college posts"""
        stmt = (
            select(Post)
            .where(
                Post.visibility == PostVisibilityEnum.COLLEGE,
                Post.college_id == college_id,
                Post.is_hidden.is_(False),
                Post.is_deleted.is_(False),
            )
            .options(joinedload(Post.user))
        )

        stmt = cursor_pagination(
            stmt=stmt,
            cursor=cursor,
            limit=limit,
            created_at_column=Post.created_at,
            id_column=Post.id,
        )

        result = await self.db.execute(stmt)
        return result.scalars().all()

    @sqlalchemy_exceptions
    async def get_public_posts(self, limit: int, cursor: str | None) -> list[Post]:
        """Get all public posts"""
        stmt = (
            select(Post)
            .where(
                Post.visibility == PostVisibilityEnum.PUBLIC,
                Post.is_hidden.is_(False),
                Post.is_deleted.is_(False),
            )
            .options(joinedload(Post.user))
        )

        stmt = cursor_pagination(
            stmt=stmt,
            cursor=cursor,
            limit=limit,
            created_at_column=Post.created_at,
            id_column=Post.id,
        )

        result = await self.db.execute(stmt)
        return result.scalars().all()

    @sqlalchemy_exceptions
    async def get_post_by_id(self, post_id: UUID, user_id: UUID) -> Post | None:
        """Get post by id"""
        stmt = (
            select(Post)
            .where(
                Post.id == post_id,
                Post.user_id == user_id,
                Post.is_hidden.is_(False),
            )
            .options(joinedload(Post.user))
        )

        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()  

    @sqlalchemy_exceptions
    async def update_post(self, post: Post) -> Post:
        """Update post"""
        await self.db.flush()
        await self.db.refresh(post)
        return post

    @sqlalchemy_exceptions
    async def delete_post(self, post: Post) -> None:
        """Soft Delete a post"""
        post.is_deleted = True
        await self.db.flush()
        await self.db.refresh(post) 

def get_feed_repository(
    db: AsyncSession = Depends(get_async_session)
) -> FeedRepository:
    return FeedRepository(db)