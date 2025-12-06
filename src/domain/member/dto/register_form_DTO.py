from pydantic import BaseModel

class RegisterFormDTO(BaseModel):
    name: str
    email: str
    password: str
