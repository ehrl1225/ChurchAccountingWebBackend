from enum import Enum

class MemberRole(Enum):
    READ_ONLY = 0
    READ_WRITE = 1
    ADMIN = 2
    OWNER = 3