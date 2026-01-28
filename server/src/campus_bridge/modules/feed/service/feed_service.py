import structlog
from uuid import UUID   
from fastapi import Depends

from campus_bridge.data.schemas.feed import PostCreate, PostResponse, PostUpdateRequest
from campus_bridge.modules.feed.repository.feed_repository import FeedRepository, get_feed_repository
from campus_bridge.data.models.post import Post
from campus_bridge.data.models.user import User
from campus_bridge.errors.exc import BadRequestError

logger = structlog.stdlib.get_logger(__name__)

class FeedService:
    def __init__(
        self, 
        repository: FeedRepository,
    ):
        self.repository = repository

    async def get_my_posts(self, current_user: User) -> list[PostResponse]:
        """Get all posts of current user"""
        posts = await self.repository.get_my_posts(current_user.id)
        logger.info("my_posts_fetched", user_id=str(current_user.id), posts=len(posts))
        return [PostResponse.model_validate(post) for post in posts]    

    async def create_post(self, post_data: PostCreate, current_user: User) -> PostResponse:
        """Create a single post"""
        post = Post(
            user_id=current_user.id,   
            college_id=current_user.college_id, 
            content=post_data.content,
            post_type=post_data.post_type,
            visibility=post_data.visibility,
            metadata=post_data.metadata
        )
        created_post = await self.repository.create_post(post)  
        logger.info(
            "post_created",
            user_id=str(current_user.id),
            post_id=str(created_post.id),
        )
        return PostResponse.model_validate(created_post)

    async def get_college_posts(self, current_user: User) -> list[PostResponse]:
        """Get all college posts"""
        posts = await self.repository.get_college_posts(college_id=current_user.college_id)
        logger.info("college_posts_fetched", user_id=str(current_user.id), posts=len(posts))  
        return [PostResponse.model_validate(post) for post in posts]

    async def get_public_posts(self, current_user: User) -> list[PostResponse]:
        """Get all public posts"""
        posts = await self.repository.get_public_posts()
        logger.info("public_posts_fetched", user_id=str(current_user.id), count=len(posts))
        return [PostResponse.model_validate(post) for post in posts]

    async def update_post(self, post_id: UUID, post_data: PostUpdateRequest, current_user: User) -> PostResponse:
        """Partial updation of a post"""
        updated_post = post_data.model_dump(exclude_unset=True)
        if not updated_post:
            logger.warning("post_update_payload_is_empty")
            raise BadRequestError(
                message="No fields provided for update",
                details="PATCH payload cannot be empty"
            )

        post = await self.repository.get_post_by_id(post_id=post_id, user_id=current_user.id)
        if not post:
            logger.warning(
                "post_not_found",
                post_id=str(post_id)
            )
            raise BadRequestError(
                message="Post not found",
                details=f"Post {post_id} does not exist"
            )

        for field, value in updated_post.items():
            setattr(post, field, value)
        
        post = await self.repository.update_post(post=post)
        logger.info(
            "post_updated",
            post_id=str(post_id),
            updated_fields=list(updated_post.keys())
        )
        return PostResponse.model_validate(post)    

    async def delete_post(self, post_id: UUID, current_user: User) -> None:
        """Delete a post by admin or officials or alumni only their posts not others posts"""
        post = await self.repository.get_post_by_id(post_id=post_id, user_id=current_user.id)
        if not post:
            logger.warning(
                "post_not_found",
                post_id=str(post_id)
            )
            raise BadRequestError(
                message="Post not found",
                details=f"Post {post_id} does not exist"
            )
        await self.repository.delete_post(post=post)
        logger.info(
            "post_deleted",
            post_id=str(post_id)
        )   

    
def get_feed_service(
    repository: FeedRepository = Depends(get_feed_repository)
) -> FeedService:
    return FeedService(repository)