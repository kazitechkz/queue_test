from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.shared.database_constants import ID, AppTableNames, CreatedAt, UpdatedAt, TableConstantsNames


class FactoryModel(Base):
    __tablename__ = AppTableNames.FactoryTableName
    id: Mapped[ID]
    title: Mapped[str] = mapped_column(Text())
    sap_id: Mapped[str] = mapped_column(String(length=TableConstantsNames.STANDARD_LENGTH_STRING), index=True, unique=True)
    status: Mapped[bool] = mapped_column(default=True)
    created_at: Mapped[CreatedAt]
    updated_at: Mapped[UpdatedAt]

    workshops: Mapped[list["WorkshopModel"]] = relationship(back_populates="factory")

    order: Mapped["OrderModel"] = relationship("OrderModel", back_populates="factory")
