from pydantic import BaseModel, EmailStr, Field
from campus_bridge.data.enums.role import RoleEnum

class RegisterRequest(BaseModel):
    college_id: uuid.UUID = Field(
        description="Selected College ID"
    )
    email: EmailStr = Field(
        description="Email ID for Register or Signup"
    )
    password: str = Field(
        min_length=8,
        description="Password for Register or Signup"
    )
    phone: str = Field(
        min_length=10,
        max_length=15,
        description="User phone number"
    )
    role: RoleEnum = Field(
        description="Role of the user (STUDENT, ALUMNI, OFFICIAL)"
    )

class LoginRequest(BaseModel):
    email: EmailStr = Field(description="Email ID for Login or Signin")
    password: str = Field(description="Password for Login or Signin")

class TokenResponse(BaseModel):
    access_token: str = Field(description="Access Token for the verification")
    token_type: str = "bearer"