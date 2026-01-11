from fastapi import APIRouter, Depends, FastAPI
from .health_check import router as health_check_router

# this is for checking the health status of the backend system 
_health_router = APIRouter()
_health_router.include_router(health_check_router)

# this is for the public router which eg. auth
# TODO(Sujal) : Create public router 
# _public_router = APIRouter()
# _public_router.include_router()

# this is for the private router
# TODO(Sujal) : Add the dependency injection after creation auth to get_current_user
# TODO(Sujal) : Automatically making the router protected without middleware  
# _private_router = APIRouter(dependencies=[Depends(get_current_user)])
# _private_router.include_router()

# this is the actual api_router which will handle all the public, private and all router
_api_router = APIRouter(prefix="/api/v1")

# _api_router.include_router(_public_router)
# _api_router.include_router(_private_router)


def add_application_routes(app: FastAPI):
    app.include_router(_health_router)
    # app.include_router(_api_router)

__all__ = ["add_application_routes"]
