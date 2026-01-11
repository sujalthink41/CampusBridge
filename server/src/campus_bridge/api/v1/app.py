from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from campus_bridge.config.lifespan import lifespan
from campus_bridge.config.settings import settings
from campus_bridge.api.v1.routes import add_application_routes


app = FastAPI(title="CollegeBridge", version="0.1.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

add_application_routes(app)
