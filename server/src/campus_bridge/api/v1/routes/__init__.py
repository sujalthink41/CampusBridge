from fastapi import APIRouter, Depends, FastAPI
from .health_check import router as health_check_router

# Import all module routers
from campus_bridge.modules.auth.router.auth import router as auth_router
from campus_bridge.modules.college.router.college_router import router as college_router
from campus_bridge.modules.feed.router.feed_router import router as feed_router
from campus_bridge.modules.users.router.user_router import router as user_router
from campus_bridge.api.v1.dependencies import get_current_user

# Health check router (no auth required)
_health_router = APIRouter()
_health_router.include_router(health_check_router)

# Public router - endpoints that don't require authentication (e.g., auth)
_public_router = APIRouter()
_public_router.include_router(auth_router)

# Private router - endpoints that require authentication
# All routes under this router automatically require get_current_user
_private_router = APIRouter(dependencies=[Depends(get_current_user)])
_private_router.include_router(college_router)
_private_router.include_router(feed_router)
_private_router.include_router(user_router)

# Main API router with /api/v1 prefix
_api_router = APIRouter(prefix="/api/v1")
_api_router.include_router(_public_router)
_api_router.include_router(_private_router)


def add_application_routes(app: FastAPI):
    """Register all application routes"""
    app.include_router(_health_router)
    app.include_router(_api_router)

__all__ = ["add_application_routes"]