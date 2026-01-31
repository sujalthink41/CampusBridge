from campus_bridge.data.schemas.alumni import CreateAlumni
from uuid import UUID
from fastapi import Depends

from campus_bridge.data.schemas.alumni import AlumniResponse, CreateAlumni, UpdateAlumni
from campus_bridge.data.models import User, Alumni
from campus_bridge.modules.alumni.repository.alumni_repository import AlumniRepository, get_alumni_repository

class AlumniService:    
    
    def __init__(
        self,
        alumni_repository: AlumniRepository,
    ):
        self.alumni_repository = alumni_repository

    async def get_current_alumni(self, current_alumni: User) -> AlumniResponse:
        """Get the current alumni profile"""

        return await self.alumni_repository.get_current_alumni(current_alumni.id)

    async def get_all_alumni(self) -> list[AlumniResponse]:
        """Get all alumni profiles"""
        
        return await self.alumni_repository.get_all_alumni()
    
    async def get_all_alumni_by_college(
        self, 
        college_id: UUID | None = None,
        skip: int = 0,
        limit: int = 100
    ) -> list[AlumniResponse]:
        """Get all alumni of a college"""

        return await self.alumni_repository.get_all_alumni_by_college(
            college_id=college_id,
            skip=skip,
            limit=limit
        )

    async def create_alumni(self, alumni: CreateAlumni, user_id: UUID) -> AlumniResponse:
        """Create a new alumni profile"""
        alumni_db = Alumni(
            user_id=user_id,
            graduation_year=alumni.graduation_year,
            company=alumni.company,
            designation=alumni.designation,
            experience_years=alumni.experience_years,
            expertise_areas=alumni.expertise_areas,
            is_available=alumni.is_available
        )
        
        alumni = await self.alumni_repository.create_alumni(alumni_db)
        return AlumniResponse.model_validate(alumni)

    async def update_alumni(self, alumni: UpdateAlumni, user_id: UUID) -> AlumniResponse:
        """Update an alumni profile"""
        alumni_db = Alumni(
            user_id=user_id,
            graduation_year=alumni.graduation_year,
            company=alumni.company,
            designation=alumni.designation,
            experience_years=alumni.experience_years,
            expertise_areas=alumni.expertise_areas,
            is_available=alumni.is_available
        )
        
        for key, value in alumni.model_dump(exclude_unset=True).items():
            setattr(alumni_db, key, value)

        alumni = await self.alumni_repository.update_alumni(alumni_db)
        return AlumniResponse.model_validate(alumni)    
    
    async def delete_alumni(self, alumni_id: UUID) -> None:
        """Delete an alumni profile"""      
        await self.alumni_repository.delete_alumni(alumni_id)

def get_alumni_service(
    alumni_repository: AlumniRepository = Depends(get_alumni_repository)
) -> AlumniService:
    return AlumniService(alumni_repository)

        
