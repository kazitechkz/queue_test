from typing import Text, List

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.shared.database_constants import AppTableNames, ID, CreatedAt, UpdatedAt


class FactoryModel:
    __tablename__ = AppTableNames.FactoryTableName
    id: Mapped[ID]
    title: Mapped[str] = mapped_column(Text())
    sap_id: Mapped[str] = mapped_column(String(length=256), index=True, unique=True)
    status: Mapped[bool] = mapped_column(default=True)
    created_at: Mapped[CreatedAt]
    updated_at: Mapped[UpdatedAt]

    workshops: Mapped[List["WorkshopModel"]] = relationship(
        back_populates="factory"
    )
