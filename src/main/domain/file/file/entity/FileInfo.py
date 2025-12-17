from sqlalchemy import String, Integer, DateTime, union_all
from sqlalchemy.orm import Mapped
from sqlalchemy.testing.schema import mapped_column
from datetime import datetime

from common.database import BaseEntity

class FileInfo(BaseEntity):
    __tablename__ = "file_info"
    file_name: Mapped[str] = mapped_column(String, nullable=False, unique=True, index=True)
    original_file_name: Mapped[str] = mapped_column(String, nullable=False)
    content_type: Mapped[str] = mapped_column(String, nullable=False)
    file_size: Mapped[int] = mapped_column(Integer, nullable=False)
    file_url: Mapped[str] = mapped_column(String, nullable=False)
    uploaded_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
