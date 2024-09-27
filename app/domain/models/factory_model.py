from typing import List

from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.shared.database_constants import AppTableNames, ID, CreatedAt, UpdatedAt


class FactoryModel(Base):
    __tablename__ = AppTableNames.FactoryTableName
    id: Mapped[ID]
    title: Mapped[str] = mapped_column(Text(length=1000))
    sap_id: Mapped[str] = mapped_column(String(length=256), index=True, unique=True)
    status: Mapped[bool] = mapped_column(default=True)
    created_at: Mapped[CreatedAt]
    updated_at: Mapped[UpdatedAt]

    workshops: Mapped[List["WorkshopModel"]] = relationship(
        back_populates="factory"
    )

    order: Mapped["OrderModel"] = relationship("OrderModel", back_populates="factory")
