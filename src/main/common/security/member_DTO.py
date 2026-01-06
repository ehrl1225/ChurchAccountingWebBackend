from pydantic import BaseModel, ConfigDict


class MemberDTO(BaseModel):
    id: int
    name: str
    email: str

    model_config = ConfigDict(from_attributes=True)