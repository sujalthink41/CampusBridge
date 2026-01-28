from uuid import UUID
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

from campus_bridge.data.enums.post import PostVisibilityEnum
from campus_bridge.data.enums.post import PostTypeEnum


class PostCreate(BaseModel):
    """This is the base model for post"""

    content: str = Field(..., min_length=1, max_length=5000, description="The content of the post")
    post_type: PostTypeEnum = Field(..., description="The type of the post")
    visibility: PostVisibilityEnum = Field(..., description="The visibility of the post")
    metadata: dict | None = Field(default_factory=dict, description="The metadata of the post")

class PostResponse(PostCreate):
    """This is the response model for post"""

    id: UUID = Field(..., description="The id of the post")
    college_id: UUID = Field(..., description="The id of the college")  
    created_at: datetime = Field(..., description="The creation time of the post")
    updated_at: datetime = Field(..., description="The update time of the post")
    user_id: UUID = Field(..., description="The id of the user who created the post")   

class PostUpdateRequest(BaseModel):
    """This is the update model for post"""

    content: Optional[str] = Field(default=None, min_length=1, max_length=5000, description="The content of the post")
    post_type: Optional[PostTypeEnum] = Field(default=None, description="The type of the post")
    visibility: Optional[PostVisibilityEnum] = Field(default=None, description="The visibility of the post")
    metadata: Optional[dict] = Field(default=None, description="The metadata of the post")  
