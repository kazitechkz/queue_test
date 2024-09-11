import decimal

from sqlalchemy import Text, String, ForeignKey, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.shared.database_constants import AppTableNames, ID, CreatedAt, UpdatedAt


class MaterialModel:
    __tablename__ = AppTableNames.MaterialTableName
    id: Mapped[ID]
    title: Mapped[str] = mapped_column(Text())
    sap_id: Mapped[str] = mapped_column(String(length=256), index=True, unique=True)
    status: Mapped[bool] = mapped_column(default=True)
    price_without_taxes: Mapped[float] = mapped_column(Numeric(precision=10, scale=2))
    price_with_taxes: Mapped[float] = mapped_column(Numeric(precision=10, scale=2))
    workshop_id: Mapped[int] = mapped_column(
        ForeignKey(AppTableNames.WorkshopTableName + ".id", ondelete="cascade", onupdate="set null"))
    workshop_sap_id: Mapped[str] = mapped_column(index=True)
    created_at: Mapped[CreatedAt]
    updated_at: Mapped[UpdatedAt]

    workshop: Mapped["WorkshopModel"] = relationship(
        back_populates="materials"
    )