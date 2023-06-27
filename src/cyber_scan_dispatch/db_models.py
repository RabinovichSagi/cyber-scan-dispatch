from sqlalchemy import String
from sqlalchemy.orm import mapped_column, Mapped

from db import Base


class ScanJob(Base):
    __tablename__ = "scan_job"

    id: Mapped[str] = mapped_column(String, primary_key=True, nullable=False)
    status: Mapped[str] = mapped_column(String, nullable=False)  # TODO: turn into ENUM
    target: Mapped[str] = mapped_column(String, nullable=False)

    def __repr__(self) -> str:
        return f'{ScanJob.__name__}(id={self.id}, status={self.status})'
