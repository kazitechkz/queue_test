from typing import Text, List

from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.shared.database_constants import ID, CreatedAt, UpdatedAt, AppTableNames


class WorkshopModel:
    __tablename__ = AppTableNames.WorkshopTableName
    id: Mapped[ID]
    title: Mapped[str] = mapped_column(Text())
    sap_id: Mapped[str] = mapped_column(String(length=256), index=True, unique=True)
    status: Mapped[bool] = mapped_column(default=True)
    factory_id: Mapped[int] = mapped_column(
        ForeignKey(AppTableNames.FactoryTableName + ".id", ondelete="cascade", onupdate="set null"))
    factory_sap_id: Mapped[str] = mapped_column(index=True)
    created_at: Mapped[CreatedAt]
    updated_at: Mapped[UpdatedAt]

    factory: Mapped["FactoryModel"] = relationship(
        back_populates="workshops"
    )

    materials: Mapped[List["MaterialModel"]] = relationship(
        back_populates="workshop"
    )