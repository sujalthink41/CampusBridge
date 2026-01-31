from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi_injectable import setup_graceful_shutdown

from .logging import initialize_logging


@asynccontextmanager
async def lifespan(app: FastAPI):
    initialize_logging()
    yield
    setup_graceful_shutdown()
