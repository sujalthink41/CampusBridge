from enum import Enum

from sqlalchemy import Enum as SQLEnum

from campus_bridge.constants.role_constants import (
    ADMIN,
    OFFICIALS,
    ALUMNI,
    STUDENT
)
from campus_bridge.utils.db_object import get_database_native_name

class RoleEnum(str, Enum):
    ADMIN = ADMIN
    OFFICIALS = OFFICIALS
    ALUMNI = ALUMNI
    STUDENT = STUDENT

role_enum = SQLEnum(
    RoleEnum,
    name=get_database_native_name("Role", "enum")
)

