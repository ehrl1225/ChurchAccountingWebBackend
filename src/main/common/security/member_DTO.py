from pydantic import BaseModel

class MemberDTO(BaseModel):
    id: int
    name: str
    email: str