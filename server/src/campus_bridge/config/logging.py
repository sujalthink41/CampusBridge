import logging 
import sys
from typing import Any 

import structlog
from structlog.types import EventDict, Processor

from .settings import settings

def add_app_context(logger: Any, method_name: str, event_dict: EventDict) -> EventDict:
    """Add application context to log events."""
    event_dict["app"] = settings.APP_NAME
    event_dict["environment"] = settings.ENVIRONMENT
    return event_dict

def setup_structlog() -> None:
    """Configue structurlog for structured JSON logging"""

    # shared processors for both structlog and stdlib
    shared_processors: list[Processor] = [
        structlog.contextvars.merge_contextvars,  # Merge context variables
        structlog.stdlib.add_log_level,  # Add log level
        structlog.stdlib.add_logger_name,  # Add logger name
        add_app_context,  # Add app metadata
        structlog.processors.TimeStamper(fmt="iso", utc=True),  # ISO 8601 timestamp
        structlog.processors.StackInfoRenderer(),  # Render stack info if present
    ]

    # build processor based on environment
    if settings.is_production:
        # production JSON output 
        final_processors = shared_processors + [
            structlog.processors.format_exc_info,  # Format exception info
            structlog.processors.UnicodeDecoder(),  # Decode bytes to unicode
            structlog.processors.JSONRenderer(),  # Render as JSON
        ]
    else:
        # Development: Human-readable console output
        final_processors = shared_processors + [
            structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
        ]

    # Configure structlog once with the appropriate processors
    structlog.configure(
        processors=final_processors,
        wrapper_class=structlog.stdlib.BoundLogger,
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        cache_logger_on_first_use=True,
    )

    # Get log level from settings
    log_level = getattr(logging, settings.LOG_LEVEL.value)

    # Configure stdlib logging
    logging.basicConfig(
        format="%(message)s",
        stream=sys.stdout,
        level=log_level,
    )

    # Create processor formatter for stdlib in development
    if not settings.is_production:
        formatter = structlog.stdlib.ProcessorFormatter(
            processors=[
                structlog.stdlib.ProcessorFormatter.remove_processors_meta,
                structlog.dev.ConsoleRenderer(colors=True),
            ],
        )

        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(formatter)
        root_logger = logging.getLogger()
        root_logger.handlers = [handler]
        root_logger.setLevel(log_level)


def initialize_logging():
    """Initialize application logging (called from lifespan)."""
    setup_structlog()

    # Set log levels for noisy libraries
    logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)
