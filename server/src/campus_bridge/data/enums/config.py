from enum import Enum

from ...constants.config_constants import (
    ENV_DEVELOPMENT,
    ENV_PRODUCTION,
    LOG_LEVEL_WARNING,
    LOG_LEVEL_INFO,
    LOG_LEVEL_ERROR,
    LOG_LEVEL_DEBUG,
    LOG_LEVEL_CRITICAL
)

class Environments(str, Enum):
    development = ENV_DEVELOPMENT
    production = ENV_PRODUCTION

class LogLevel(str, Enum):
    DEBUG = LOG_LEVEL_DEBUG
    WARNING = LOG_LEVEL_WARNING
    INFO = LOG_LEVEL_INFO
    ERROR = LOG_LEVEL_ERROR
    CRITICAL = LOG_LEVEL_CRITICAL