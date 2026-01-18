from datetime import datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, Field

from campus_bridge.data.enums.state import StateEnum

class CreateCollegeRequest(BaseModel):
    """This is for Creating College Request schema"""
    name: str = Field(description="Name of the College")
    is_government: bool = Field(default=False, description="Type of college government or private")
    state: StateEnum = Field(description="State in which college is present")
    city: str = Field(description="City in which college is present")

    class Config:
        from_attributes = True

class CollegeResponse(CreateCollegeRequest):
    """This is for Validating the response of the College Schema"""
    id: UUID = Field(description="Unique identifier for the college")
    created_at: datetime = Field(description="Created time of college")
    updated_at: datetime = Field(description="Updated time of the college")

    class Config:
        from_attributes = True


class CollegeUpdateRequest(BaseModel):
    """Schema for partially updating a college"""

    name: Optional[str] = Field(
        default=None,
        description="Name of the college"
    )
    is_government: Optional[bool] = Field(
        default=None,
        description="Whether the college is government or private"
    )
    state: Optional[StateEnum] = Field(
        default=None,
        description="State in which the college is present"
    )
    city: Optional[str] = Field(
        default=None,
        description="City in which the college is present"
    )

    class Config:
        from_attributes = True

class CollegeDeleteResponse(BaseModel):
    """Delete college response"""
    message: str = Field(
        description="Message confirming college deletion"
    )