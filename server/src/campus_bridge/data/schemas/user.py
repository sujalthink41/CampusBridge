from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, EmailStr, Field

from campus_bridge.data.enums.role import RoleEnum


class UserResponse(BaseModel):
    id: UUID = Field(description="User unique identifier")
    email: EmailStr = Field(description="User email")
    phone: str = Field(description="User phone number")
    role: RoleEnum = Field(description="Role of the user")
    college_id: UUID = Field(description="Associated college ID")
    is_verified: bool = Field(description="Whether user is verified")

    class Config:
        from_attributes = True  
