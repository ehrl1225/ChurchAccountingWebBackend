from sqlalchemy import Column, Integer, String, Boolean

from common.database import Base

class Member(Base):
    __tablename__ = 'member'
    id: int = Column(Integer, primary_key=True, autoincrement=True)
    name: str = Column(String, unique=True, nullable=False)
    email: str = Column(String, unique=True, nullable=False)
    hashed_password: str = Column(String)
    email_verified: bool = Column(Boolean)