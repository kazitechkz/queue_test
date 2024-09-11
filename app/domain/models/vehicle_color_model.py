from sqlalchemy import String
from sqlalchemy.orm import mapped_column, Mapped, relationship

from app.core.database import Base
from app.shared.database_constants import AppTableNames, UpdatedAt, CreatedAt, ID


class VehicleColorModel(Base):
    __tablename__ = AppTableNames.VehicleColorTableName
    id: Mapped[ID]
    title: Mapped[str] = mapped_column(String(length=200))
    value: Mapped[str] = mapped_column(String(length=255), unique=True)
    created_at: Mapped[CreatedAt]
    updated_at: Mapped[UpdatedAt]

    vehicles: Mapped[list["VehicleModel"]] = relationship(
        back_populates="color"
    )
