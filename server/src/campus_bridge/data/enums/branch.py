from enum import Enum

from sqlalchemy import Enum as SQLEnum

from campus_bridge.constants.branch_contants import (
    CIVIL,
    CSE,
    ECE,
    ELECTRICAL,
    IT,
    MECHNICAL,
)
from campus_bridge.utils.db_object import get_database_native_name


class BranchEnum(str, Enum):
    CSE = CSE
    IT = IT
    CIVIL = CIVIL
    MECHNICAL = MECHNICAL
    ELECTRICAL = ELECTRICAL
    ECE = ECE


branch_enum = SQLEnum(BranchEnum, name=get_database_native_name("Branch", "enum"))
