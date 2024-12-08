from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.shared.database_constants import ID, AppTableNames, CreatedAt, UpdatedAt, TableConstantsNames


class RegionModel(Base):
    __tablename__ = AppTableNames.RegionTableName
    id: Mapped[ID]
    title: Mapped[str] = mapped_column(String(length=TableConstantsNames.STANDARD_LENGTH_STRING))
    value: Mapped[str] = mapped_column(String(length=TableConstantsNames.STANDARD_LENGTH_STRING), unique=True)
    created_at: Mapped[CreatedAt]
    updated_at: Mapped[UpdatedAt]

    vehicles: Mapped[list["VehicleModel"]] = relationship(back_populates="region")
