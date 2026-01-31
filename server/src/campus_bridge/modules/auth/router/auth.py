from fastapi import APIRouter, Depends, status

from campus_bridge.data.schemas.auth import LoginRequest, RegisterRequest, TokenResponse
from campus_bridge.modules.auth.service.auth import AuthService, get_auth_service

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(
    payload: RegisterRequest, service: AuthService = Depends(get_auth_service)
):
    return await service.register(payload=payload)


@router.post("/login", response_model=TokenResponse, status_code=status.HTTP_200_OK)
async def login(
    payload: LoginRequest, service: AuthService = Depends(get_auth_service)
):
    return await service.login(payload=payload)
