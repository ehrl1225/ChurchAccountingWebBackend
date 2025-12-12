from pydantic import BaseModel

class MemberDTO(BaseModel):
    id: int
    email: str