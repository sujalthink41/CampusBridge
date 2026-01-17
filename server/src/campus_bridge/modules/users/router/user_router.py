from fastapi import APIRouter, status, Depends

from campus_bridge.data.models.user import User
from campus_bridge.api.v1.dependencies import get_current_user
from campus_bridge.data.schemas.user import UserResponse

router = APIRouter("/user", tags=["users"])

@router.get("", status_code=status.HTTP_200_OK, response_model=UserResponse)
async def get_user(
    current_user: User = Depends(get_current_user)
): 
    return current_user
