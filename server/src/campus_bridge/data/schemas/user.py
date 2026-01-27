from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, EmailStr, Field

from campus_bridge.data.enums.role import RoleEnum

class UserResponse(BaseModel):
    """This is the response after creation of user"""
    id: UUID = Field(description="User unique identifier")
    email: EmailStr = Field(description="User email")
    phone: str = Field(description="User phone number")
    role: RoleEnum = Field(description="Role of the user")
    college_id: UUID = Field(description="Associated college ID")
    is_verified: bool = Field(description="Whether user is verified")

    class Config:
        from_attributes = True  

class UserUpdateRequest(BaseModel):
    """This is the UserUpdateRequest Schema"""
    phone: Optional[str] = Field(default=None, description="User updated phone number")
    role: Optional[RoleEnum] = Field(default=None, description="User updated role") 

class UserUpdateResponse(UserResponse):
    """This is the UserUpdateResponse Schema"""
    pass