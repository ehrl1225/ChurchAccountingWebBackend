from pydantic import BaseModel

class LoginFormDTO(BaseModel):
    email: str
    password: str