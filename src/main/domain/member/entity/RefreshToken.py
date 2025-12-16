from datetime import datetime

from sqlalchemy import String, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from common.database import BaseEntity

class RefreshToken(BaseEntity):
    __tablename__ = "refresh_token"
    hashed_token: Mapped[str] = mapped_column(String)
    jti: Mapped[str] = mapped_column(String, unique=True)
    issued_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    expires_at: Mapped[datetime] = mapped_column(DateTime)
    ip_address: Mapped[str] = mapped_column(String)
    user_agent: Mapped[str] = mapped_column(String)
    member_id: Mapped[int] = mapped_column(ForeignKey("member.id"))

    member: Mapped["Member"] = relationship(
        "Member",
        back_populates="refresh_tokens"
    )