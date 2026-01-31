from uuid import UUID

from fastapi import APIRouter, Depends, Query, status

from campus_bridge.api.v1.dependencies import (
    get_current_user,
    require_admin_or_officials_or_alumni,
)
from campus_bridge.data.models.user import User
from campus_bridge.data.schemas.feed import PostCreate, PostResponse, PostUpdateRequest
from campus_bridge.modules.feed.service.feed_service import (
    FeedService,
    get_feed_service,
)

router = APIRouter(prefix="/feed", tags=["feed"])


@router.get("/me", status_code=status.HTTP_200_OK, response_model=list[PostResponse])
async def get_my_posts(
    current_user: User = Depends(get_current_user),
    feed_service: FeedService = Depends(get_feed_service),
):
    """Current User posts"""
    return await feed_service.get_my_posts(current_user)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=PostResponse)
async def create_post(
    post_data: PostCreate,
    current_user: User = Depends(require_admin_or_officials_or_alumni),
    feed_service: FeedService = Depends(get_feed_service),
):
    """Create a new post by admin or officials or alumni"""
    return await feed_service.create_post(post_data, current_user)


@router.get(
    "/college", status_code=status.HTTP_200_OK, response_model=list[PostResponse]
)
async def get_all_posts_by_college(
    current_user: User = Depends(get_current_user),
    feed_service: FeedService = Depends(get_feed_service),
    limit: int = Query(default=10, ge=1, le=50),
    cursor: str | None = Query(None, description="Cursor for pagination"),
):
    """Current User college specific posts"""
    return await feed_service.get_college_posts(
        current_user=current_user, limit=limit, cursor=cursor
    )


@router.get(
    "/public", status_code=status.HTTP_200_OK, response_model=list[PostResponse]
)
async def get_public_posts(
    current_user: User = Depends(get_current_user),
    feed_service: FeedService = Depends(get_feed_service),
    limit: int = Query(default=10, ge=1, le=50),
    cursor: str | None = Query(None, description="Cursor for pagination"),
):
    """Public feed"""
    return await feed_service.get_public_posts(
        current_user=current_user, limit=limit, cursor=cursor
    )


@router.patch("/{post_id}", status_code=status.HTTP_200_OK, response_model=PostResponse)
async def update_post(
    post_id: UUID,
    post_data: PostUpdateRequest,
    current_user: User = Depends(require_admin_or_officials_or_alumni),
    feed_service: FeedService = Depends(get_feed_service),
):
    """Update a post by admin or officials or alumni only their posts not others posts"""
    return await feed_service.update_post(post_id, post_data, current_user)


@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(
    post_id: UUID,
    current_user: User = Depends(require_admin_or_officials_or_alumni),
    feed_service: FeedService = Depends(get_feed_service),
):
    """Delete a post by admin or officials or alumni only their posts not others posts"""
    return await feed_service.delete_post(post_id, current_user)
