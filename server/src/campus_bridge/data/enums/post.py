from enum import Enum 
from sqlalchemy import Enum as SQLEnum

from campus_bridge.utils.db_object import get_database_native_name
from campus_bridge.constants.post_contstant import (
    TEXT,
    ANNOUNCEMENT,
    OPPORTUNITY,
    QUERY,
    EVENT,
    PUBLIC,
    COLLEGE
)

class PostTypeEnum(str, Enum):
    # type of post enum 
    TEXT = TEXT
    ANNOUNCEMENT = ANNOUNCEMENT
    OPPORTUNITY = OPPORTUNITY
    QUERY = QUERY
    EVENT = EVENT 

post_type_enum = SQLEnum(
    PostTypeEnum,
    name=get_database_native_name("PostType", "enum")
)

class PostVisibilityEnum(str, Enum):
    # visibility to whom enum 
    PUBLIC = PUBLIC
    COLLEGE = COLLEGE 

post_visibility_type_enum = SQLEnum(
    PostVisibilityEnum,
    name=get_database_native_name("PostVisibility", "enum")
)