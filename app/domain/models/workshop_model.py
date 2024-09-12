from typing import List

from sqlalchemy import String, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.shared.database_constants import ID, CreatedAt, UpdatedAt, AppTableNames


class WorkshopModel(Base):
    __tablename__ = AppTableNames.WorkshopTableName
    id: Mapped[ID]
    title: Mapped[str] = mapped_column(Text(length=1000))
    sap_id: Mapped[str] = mapped_column(String(length=256), index=True, unique=True)
    status: Mapped[bool] = mapped_column(default=True)
    factory_id: Mapped[int] = mapped_column(
        ForeignKey(AppTableNames.FactoryTableName + ".id", ondelete="set null", onupdate="cascade"),nullable=True)
    factory_sap_id: Mapped[str] = mapped_column(String(length=256),index=True)
    created_at: Mapped[CreatedAt]
    updated_at: Mapped[UpdatedAt]

    factory: Mapped["FactoryModel"] = relationship(
        back_populates="workshops"
    )

    materials: Mapped[List["MaterialModel"]] = relationship(
        back_populates="workshop"
    )