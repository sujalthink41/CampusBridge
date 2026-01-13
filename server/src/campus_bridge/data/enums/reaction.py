from enum import Enum 
from sqlalchemy import Enum as SQLEnum

from campus_bridge.utils.db_object import get_database_native_name
from campus_bridge.constants.reaction_contstant import (
    HE_HE,
    OFO,
    DAMN,
    LOVE_IT
)

class ReactionTypeEnum(str, Enum):
    # reaction enum 
    HE_HE = HE_HE
    LOVE_IT = LOVE_IT
    DAMN = DAMN
    OFO = OFO

reaction_type_enum = SQLEnum(
    ReactionTypeEnum,
    name=get_database_native_name("ReactionType", "enum")
)