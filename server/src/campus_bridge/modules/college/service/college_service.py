import structlog
from uuid import UUID

from fastapi import Depends

from campus_bridge.data.models.college import College
from campus_bridge.modules.college.repository.college_repository import CollegeRepository, get_college_repository
from campus_bridge.data.schemas.college import (
    CreateCollegeRequest,
    CollegeResponse,
    CollegeUpdateRequest,
    CollegeDeleteResponse
)
from campus_bridge.errors.exc.base_errors import BadRequestError

logger = structlog.stdlib.get_logger(__name__)

class CollegeService:
    def __init__(
        self,
        repository: CollegeRepository
    ):
        self.repository = repository

    async def create_colleges(self, payload: list[CreateCollegeRequest]) -> list[CollegeResponse]:
        """Create one or multiple colleges"""
        
        if not payload:
            logger.warning(
                "college_bulk_create_empty_payload",
                payload_length=len(payload)
            )
            raise BadRequestError(
                message="College list cannot be empty",
                details="College list must not be empty"
            )
            
        # Deserialization : Pydantic -> SQLAlchemy
        colleges = [
            College(**college.model_dump())
            for college in payload
        ]

        # DB Operation 
        colleges = await self.repository.create_colleges(colleges=colleges)
        logger.info(
            "college_bulk_create_success",
            total_colleges=len(colleges)
        )
        
        # Serialization : SQLAlchemy -> Pydantic
        return [
            CollegeResponse.model_validate(college)
            for college in colleges
        ]

    async def update_college(
        self,
        college_id: UUID,
        payload: CollegeUpdateRequest
    ) -> CollegeResponse:
        """Partially update single college"""
        update_data = payload.model_dump(exclude_unset=True)
        if not update_data:
            logger.warning("college_update_payload_is_empty")
            raise BadRequestError(
                message="No fields provided for update",
                details="PATCH payload cannot be empty"
            )

        college = await self.repository.get_college_by_id(college_id=college_id)
        if not college:
            logger.warning(
                "college_not_found",
                college_id=str(college_id),
            )
            raise BadRequestError(
                message="College not found",
                details=f"College {college_id} does not exist"
            )

        for field, value in update_data.items():
            setattr(college, field, value)
        
        college = await self.repository.update_college(college=college)
        logger.info(
            "college_updated",
            college_id=str(college_id),
            updated_fields=list(update_data.keys())
        )
        return CollegeResponse.model_validate(college)

    async def delete_college(
        self,
        college_id: UUID
    ):
        """Delete a college (soft delete)"""
        college = await self.repository.get_college_by_id(college_id=college_id)
        if not college:
            logger.warning(
                "college_not_found",
                college_id=str(college_id)
            )
            raise BadRequestError(
                message="College not found",
                details=f"College {college_id} does not exist"
            )

        await self.repository.delete_college(college=college)
        logger.info("college_deleted", college_id=str(college_id))
        return CollegeDeleteResponse(
            message=f"College {college_id} successfully deleted"
        )

    async def get_college_by_id(
        self,
        college_id: UUID
    ):
        """Get a single college"""
        college = await self.repository.get_college_by_id(college_id=college_id)
        if not college:
            logger.warning(
                "college_not_found",
                college_id=str(college_id)
            )
            raise BadRequestError(
                message="College not found",
                details=f"College {college_id} does not exist"
            )

        logger.info("college_fetched_successfully", college_id=str(college_id))
        return CollegeResponse.model_validate(college)

    async def get_all_college(
        self
    ):
        """Get all college"""
        colleges = await self.repository.get_all_college()
        logger.info("Colleges_fetched_successfully", total_colleges=len(colleges))
        return [
            CollegeResponse.model_validate(college)
            for college in colleges
        ]


def get_college_service(
    repository: CollegeRepository = Depends(get_college_repository)
) -> CollegeService:
    return CollegeService(repository=repository)