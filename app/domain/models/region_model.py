from sqlalchemy import String
from sqlalchemy.orm import mapped_column, Mapped

from app.core.database import Base
from app.shared.database_constants import AppTableNames, UpdatedAt, CreatedAt, ID

class RegionModel(Base):
    __tablename__ = AppTableNames.RegionTableName
    id: Mapped[ID]
    title: Mapped[str] = mapped_column(String(length=200))
    value: Mapped[str] = mapped_column(String(length=255), unique=True)
    created_at: Mapped[CreatedAt]
    updated_at: Mapped[UpdatedAt]