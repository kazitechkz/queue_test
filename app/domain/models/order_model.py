import datetime
from typing import Optional, List

from sqlalchemy import Integer, Computed, Numeric, Boolean, Date, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.shared.database_constants import AppTableNames, ID, CreatedAt, UpdatedAt


class OrderModel(Base):
    __tablename__ = AppTableNames.OrderTableName
    id: Mapped[ID]
    status_id: Mapped[int] = mapped_column(
        ForeignKey(AppTableNames.OrderStatusTableName + ".id", onupdate="cascade", ondelete="set null"), nullable=True)

    factory_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey(AppTableNames.FactoryTableName + ".id", onupdate="cascade", ondelete="set null"), nullable=True)
    factory_sap_id: Mapped[str] = mapped_column(String(length=256), index=True)

    workshop_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey(AppTableNames.WorkshopTableName + ".id", onupdate="cascade", ondelete="set null"), nullable=True)
    workshop_sap_id: Mapped[str] = mapped_column(String(length=256), index=True)

    material_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey(AppTableNames.MaterialTableName + ".id", onupdate="cascade", ondelete="set null"), nullable=True)
    material_sap_id: Mapped[str] = mapped_column(String(length=256), index=True)

    quan_t: Mapped[int] = mapped_column(Integer())
    quan: Mapped[int] = mapped_column(Computed("quan_t * 1000"))
    quan_released: Mapped[int] = mapped_column(Integer(), default=0)
    quan_booked: Mapped[int] = mapped_column(Integer(), default=0)
    quan_left: Mapped[int] = mapped_column(Computed("quan - quan_booked - quan_released"))
    executed_cruise: Mapped[int] = mapped_column(Integer(), default=0)

    price_without_taxes: Mapped[float] = mapped_column(Numeric(precision=10, scale=2))
    price_with_taxes: Mapped[float] = mapped_column(Numeric(precision=10, scale=2))

    sap_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey(AppTableNames.SAPRequestTableName + ".id", onupdate="cascade", ondelete="set null"), nullable=True)
    zakaz: Mapped[str] = mapped_column(String(length=20), index=True,nullable=True)

    kaspi_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey(AppTableNames.KaspiPaymentsTableName + ".id", onupdate="cascade", ondelete="set null"), nullable=True)
    txn_id: Mapped[str] = mapped_column(String(length=20), index=True, nullable=True)


    owner_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey(AppTableNames.UserTableName + ".id", onupdate="cascade", ondelete="set null"), nullable=True)
    iin: Mapped[str] = mapped_column(String(12), index=True, nullable=True)
    name: Mapped[str] = mapped_column(String(255), nullable=True)

    organization_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey(AppTableNames.OrganizationTableName + ".id", onupdate="cascade", ondelete="set null"), nullable=True)
    bin: Mapped[str] = mapped_column(String(12), index=True, nullable=True)
    dogovor: Mapped[str] = mapped_column(String(255), index=True, nullable=True)

    is_active: Mapped[bool] = mapped_column(Boolean(), default=True)
    is_finished: Mapped[bool] = mapped_column(Boolean(), default=False)
    is_failed: Mapped[bool] = mapped_column(Boolean(), default=False)
    is_paid: Mapped[bool] = mapped_column(Boolean(), default=False)

    start_at: Mapped[CreatedAt]
    end_at: Mapped[datetime] = mapped_column(Date)
    finished_at: Mapped[Optional[datetime]] = mapped_column(Date, default=None, nullable=True)
    paid_at: Mapped[Optional[datetime]] = mapped_column(Date, default=None, nullable=True)

    created_at: Mapped[CreatedAt]
    updated_at: Mapped[UpdatedAt]

    organization: Mapped["OrganizationModel"] = relationship(
        back_populates="orders",
    )

    sap_request: Mapped["SapRequestModel"] = relationship(
        "SapRequestModel",
        back_populates="order",
        primaryjoin="and_(SapRequestModel.order_id == OrderModel.id, SapRequestModel.is_failed == False)",
        foreign_keys="[SapRequestModel.order_id]",
        uselist=False,
    )

    sap_request_failed:Mapped[List["SapRequestModel"]] = relationship(
        "SapRequestModel",
        back_populates="order",
        primaryjoin="and_(SapRequestModel.order_id == OrderModel.id, SapRequestModel.is_failed == True)",
        foreign_keys="[SapRequestModel.order_id]",
        uselist=True,
    )
