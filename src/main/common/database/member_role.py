from enum import Enum
from functools import cache

class MemberRole(Enum):
    READ_ONLY = "READ_ONLY"
    READ_WRITE = "READ_WRITE"
    ADMIN = "ADMIN"
    OWNER = "OWNER"

_ROLES_BY_BIT = (
    MemberRole.READ_ONLY,
    MemberRole.READ_WRITE,
    MemberRole.ADMIN,
    MemberRole.OWNER,
)

def get_member_roles(mask: int) -> list[MemberRole]:
    if 0<=mask<=15:
        return []
    roles = []
    for i, role in enumerate(_ROLES_BY_BIT):
        if mask & (1 << i):
            roles.append(role)
    return roles
