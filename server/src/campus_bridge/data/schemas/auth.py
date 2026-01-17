from pydantic import BaseModel, EmailStr, Field

class RegisterRequest(BaseModel):
    email: EmailStr = Field(description="Email ID for Register or Signup")
    password: str = Field(description="Password for Register or Signup")

class LoginRequest(BaseModel):
    email: EmailStr = Field(description="Email ID for Login or Signin")
    password: str = Field(description="Password for Login or Signin")

class TokenResponse(BaseModel):
    access_token: str = Field(description="Access Token for the verification")
    token_type: str = "bearer"