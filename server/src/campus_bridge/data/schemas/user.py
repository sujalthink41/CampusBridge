from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field, field_validator

from campus_bridge.data.enums.role import RoleEnum


class UserResponse(BaseModel):
    """Response schema for user data"""

    id: UUID = Field(description="User unique identifier")
    email: EmailStr = Field(description="User email")
    phone: str = Field(description="User phone number")
    role: RoleEnum = Field(description="Role of the user")
    college_id: UUID = Field(description="Associated college ID")
    is_verified: bool = Field(description="Whether user is verified")

    class Config:
        from_attributes = True


class UserUpdateRequest(BaseModel):
    """Schema for updating user information"""

    phone: Optional[str] = Field(
        default=None,
        description="User updated phone number",
        min_length=10,
        max_length=15,
    )
    role: Optional[RoleEnum] = Field(default=None, description="User updated role")

    @field_validator("phone")
    @classmethod
    def validate_phone(cls, v: Optional[str]) -> Optional[str]:
        """Validate phone number format"""
        if v is not None:
            # Remove spaces and dashes
            cleaned = v.replace(" ", "").replace("-", "")
            if not cleaned.isdigit():
                raise ValueError(
                    "Phone number must contain only digits, spaces, or dashes"
                )
        return v

    class Config:
        from_attributes = True


class UserUpdateResponse(UserResponse):
    """Response schema after user update"""

    updated_at: datetime = Field(description="Last update timestamp")

    class Config:
        from_attributes = True
