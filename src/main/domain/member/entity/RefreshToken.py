from datetime import datetime

from sqlalchemy import String, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from common.database import BaseEntity

class RefreshToken(BaseEntity):
    __tablename__ = "refresh_token"
    hashed_token: Mapped[str] = mapped_column(String, nullable=False)
    jti: Mapped[str] = mapped_column(String, nullable=False, unique=True, index=True)
    issued_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.now)
    expires_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    ip_address: Mapped[str] = mapped_column(String, nullable=True)
    user_agent: Mapped[str] = mapped_column(String, nullable=True)
    member_id: Mapped[int] = mapped_column(ForeignKey("member.id"), nullable=False)

    member: Mapped["Member"] = relationship(
        "Member",
        back_populates="refresh_tokens"
    )