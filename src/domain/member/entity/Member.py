from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import Mapped, mapped_column

from common.database import BaseEntity

class Member(BaseEntity):
    __tablename__ = 'member'
    type: Mapped[str] = mapped_column(String)
    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(64))
    email_verified: Mapped[bool] = mapped_column(Boolean, default=False)

    __mapper_args__ = {
        "polymorphic_on": type,
        "polymorphic_identity": "member",
    }