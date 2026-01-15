from typing import Optional

from sqlalchemy import String, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, relationship
from sqlalchemy.testing.schema import mapped_column
from datetime import datetime

from common.database import BaseEntity

class FileInfo(BaseEntity):
    __tablename__ = "file_info"
    file_name: Mapped[str] = mapped_column(String, nullable=False, unique=True, index=True)
    organization_id: Mapped[int] = mapped_column(ForeignKey("organization.id"), nullable=False)
    receipt_id: Mapped[Optional[int]] = mapped_column(ForeignKey("receipt.id", ondelete="SET NULL"), nullable=True)
    uploaded_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.now)

    organization: Mapped['Organization'] = relationship(
        "Organization",
        back_populates="files"
    )

    receipt: Mapped['Receipt'] = relationship(
        "Receipt",
        back_populates="file"
    )
