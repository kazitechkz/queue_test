from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base
from app.shared.database_constants import ID, AppTableNames, CreatedAt, UpdatedAt, TableConstantsNames


class FileModel(Base):
    __tablename__ = AppTableNames.FileTableName
    id: Mapped[ID]
    url: Mapped[str] = mapped_column(String(TableConstantsNames.STANDARD_LENGTH_STRING), nullable=False)
    extension: Mapped[str] = mapped_column(String(TableConstantsNames.STANDARD_LENGTH_STRING), nullable=False)
    created_at: Mapped[CreatedAt]
    updated_at: Mapped[UpdatedAt]
