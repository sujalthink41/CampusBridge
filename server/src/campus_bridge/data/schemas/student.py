from uuid import UUID
from typing import Optional
from datetime import datetime
from pydantic import Field, BaseModel, ConfigDict

from campus_bridge.data.enums.branch import BranchEnum
from campus_bridge.data.enums.role import RoleEnum

class StudentBase(BaseModel):
    """Base schema for student"""

    first_name: str = Field(description="First name")
    middle_name: Optional[str] = Field(description="Middle name")
    last_name: Optional[str] = Field(description="Last name")
    roll_number: str = Field(description="Roll number")
    branch: BranchEnum = Field(description="Branch")
    year_of_study: int = Field(description="Year of study")
    id_card_url: str = Field(description="Id card url")
    interests: dict = Field(description="Interests")

    model_config = ConfigDict(from_attributes=True)

class UserBase(BaseModel):
    """Base schema for user"""

    email: str = Field(description="Email")
    role: RoleEnum = Field(description="Role")
    college_id: UUID = Field(description="College id")
    phone: str = Field(description="Phone")
    is_verified: bool = Field(description="Is verified")

    model_config = ConfigDict(from_attributes=True)

class UserResponse(UserBase):
    """Response schema for user"""

    id: UUID = Field(description="User id")

    model_config = ConfigDict(from_attributes=True)

class StudentUserResponse(BaseModel):   
    """Response schema for student user"""
    
    student: "StudentResponse"
    user: UserResponse

    model_config = ConfigDict(from_attributes=True)

class StudentCreate(StudentBase):
    """Create schema for student"""
    pass

class StudentResponse(StudentBase):
    """Response schema for student"""

    id: UUID = Field(description="Student id")
    created_at: datetime = Field(description="Created at")
    updated_at: datetime = Field(description="Updated at")

    model_config = ConfigDict(from_attributes=True)  

class StudentUpdateRequest(BaseModel):
    """Update schema for student"""
    first_name: Optional[str] = Field(description="First name")
    middle_name: Optional[str] = Field(description="Middle name")
    last_name: Optional[str] = Field(description="Last name")
    roll_number: Optional[str] = Field(description="Roll number")
    branch: Optional[BranchEnum] = Field(description="Branch")
    year_of_study: Optional[int] = Field(description="Year of study")
    interests: Optional[dict] = Field(description="Interests")

    model_config = ConfigDict(from_attributes=True)

class StudentUpdateResponse(StudentUpdateRequest):
    """Response schema for student update"""
    pass