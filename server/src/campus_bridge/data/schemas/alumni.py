from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field


class AlumniBase(BaseModel):
    """Base model for alumni"""

    graduation_year: int = Field(description="Graduation year of the alumni")
    company: str = Field(description="Company name of the alumni")
    designation: str = Field(description="Designation of the alumni")
    experience_years: int = Field(description="Experience years of the alumni")
    expertise_areas: dict = Field(description="Expertise areas of the alumni")
    is_available: bool = Field(description="Is the alumni available for mentorship")


class CreateAlumni(AlumniBase):
    """Create model for alumni"""

    user_id: Optional[UUID] = Field(None, description="User ID for the alumni profile")
    college_id: Optional[UUID] = Field(
        None, description="College ID for the alumni profile"
    )


class AlumniResponse(AlumniBase):
    """Response model for alumni"""

    id: UUID = Field(description="ID of the alumni")
    created_at: datetime = Field(description="Created at")
    updated_at: datetime = Field(description="Updated at")

    class Config:
        orm_mode = True


class UpdateAlumni(BaseModel):
    """Update model for alumni"""

    graduation_year: Optional[int] = Field(description="Graduation year of the alumni")
    company: Optional[str] = Field(description="Company name of the alumni")
    designation: Optional[str] = Field(description="Designation of the alumni")
    experience_years: Optional[int] = Field(
        description="Experience years of the alumni"
    )
    expertise_areas: Optional[dict] = Field(description="Expertise areas of the alumni")
    is_available: Optional[bool] = Field(
        description="Is the alumni available for mentorship"
    )


class UpdateAlumniResponse(UpdateAlumni):
    """Update response model for alumni"""

    pass
