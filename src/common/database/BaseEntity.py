from sqlalchemy import Column, Integer
from sqlalchemy.orm import Mapped, mapped_column

from common.database import Base

class BaseEntity(Base):
    __abstract__ = True
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
