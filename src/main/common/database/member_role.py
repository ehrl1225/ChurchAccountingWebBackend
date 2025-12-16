from enum import Enum

class MemberRole(Enum):
    READ_ONLY = "READ_ONLY"
    READ_WRITE = "READ_WRITE"
    ADMIN = "ADMIN"
    OWNER = "OWNER"