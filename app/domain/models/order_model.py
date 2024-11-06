from datetime import datetime
from typing import Optional, List

from sqlalchemy import Integer, Computed, Numeric, Boolean, Date, ForeignKey, String, DateTime, and_
from sqlalchemy.orm import Mapped, mapped_column, relationship, remote, foreign

from app.core.database import Base
from app.domain.models.factory_model import FactoryModel
from app.domain.models.kaspi_payment_model import KaspiPaymentModel
from app.domain.models.material_model import MaterialModel
from app.domain.models.organization_model import OrganizationModel
from app.domain.models.sap_request_model import SapRequestModel
from app.domain.models.workshop_model import WorkshopModel
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

    quan_t: Mapped[float] = mapped_column(Numeric(precision=10, scale=2))
    quan: Mapped[int] = mapped_column(Computed("quan_t * 1000"))
    quan_released: Mapped[int] = mapped_column(Integer(), default=0)
    quan_released_t: Mapped[float] = mapped_column(Computed("quan_released / 1000"))
    quan_booked: Mapped[int] = mapped_column(Integer(), default=0)
    quan_booked_t: Mapped[float] = mapped_column(Computed("quan_booked / 1000"))
    quan_left: Mapped[int] = mapped_column(Computed("quan - quan_booked - quan_released"))
    quan_left_t: Mapped[float] = mapped_column(Computed("quan_left / 1000"))

    executed_cruise: Mapped[int] = mapped_column(Integer(), default=0)

    price_without_taxes: Mapped[float] = mapped_column(Numeric(precision=10, scale=2))
    price_with_taxes: Mapped[float] = mapped_column(Numeric(precision=10, scale=2))

    sap_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey(AppTableNames.SAPRequestTableName + ".id", onupdate="cascade", ondelete="set null"), nullable=True)
    zakaz: Mapped[str] = mapped_column(String(length=20), index=True, nullable=True)

    kaspi_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey(AppTableNames.KaspiPaymentsTableName + ".id", onupdate="cascade", ondelete="set null"),
        nullable=True)
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

    checked_payment_by_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey(AppTableNames.UserTableName + ".id", onupdate="cascade", ondelete="set null"), nullable=True)
    checked_payment_by: Mapped[Optional[str]] = mapped_column(String(length=255), nullable=True)
    checked_payment_at: Mapped[Optional[datetime]] = mapped_column(Date, nullable=True)

    created_at: Mapped[CreatedAt]
    updated_at: Mapped[UpdatedAt]
    must_paid_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(),
        Computed("created_at + INTERVAL 1 DAY"),
        nullable=True
    )

    material: Mapped["MaterialModel"] = relationship(
        "MaterialModel"
    )

    organization: Mapped["OrganizationModel"] = relationship(
        back_populates="orders",
    )

    factory: Mapped["FactoryModel"] = relationship("FactoryModel", back_populates="order", foreign_keys=[factory_id])
    workshop: Mapped["WorkshopModel"] = relationship("WorkshopModel", foreign_keys=[workshop_id])
    kaspi: Mapped["KaspiPaymentModel"] = relationship("KaspiPaymentModel", foreign_keys=[kaspi_id])
    owner: Mapped["UserModel"] = relationship("UserModel", back_populates="orders", foreign_keys=[owner_id])

    # Связь с SapRequestModel для "успешного" запроса
    sap_request: Mapped["SapRequestModel"] = relationship(
        "SapRequestModel",
        back_populates="order",
        foreign_keys=[SapRequestModel.order_id],
        primaryjoin="and_(SapRequestModel.order_id == OrderModel.id, SapRequestModel.is_failed == False)",
        viewonly=True,
        uselist=False,
        overlaps="sap_request_failed"  # Указываем, что эта связь перекрывается с sap_request_failed
    )

    # Связь с SapRequestModel для "неудачного" запроса
    sap_request_failed: Mapped[List["SapRequestModel"]] = relationship(
        "SapRequestModel",
        back_populates="order_failed",
        foreign_keys=[SapRequestModel.order_id],
        uselist=True,
        overlaps="sap_request",  # Указываем, что эта связь перекрывается с sap_request
        viewonly=True,
        primaryjoin="and_(SapRequestModel.order_id == OrderModel.id, SapRequestModel.is_failed == True)",
    )

    # Акт взвешивания
    act_weights: Mapped[List["ActWeightModel"]] = relationship(
        "ActWeightModel",
        back_populates="order",
        foreign_keys="[ActWeightModel.order_id]"
    )

    # Первоначальное взвешивание
    initial_weights: Mapped[List["InitialWeightModel"]] = relationship(
        "InitialWeightModel",
        back_populates="order",
        foreign_keys="[InitialWeightModel.order_id]"
    )

    # Kaspi Payments
    kaspi_payment: Mapped["KaspiPaymentModel"] = relationship(
        "KaspiPaymentModel",
        back_populates="order",
        foreign_keys="[KaspiPaymentModel.order_id]",
        uselist=False,
        primaryjoin="and_(KaspiPaymentModel.order_id == OrderModel.id, KaspiPaymentModel.is_paid == True)",
        overlaps="kaspi_payment_failed"  # Указываем, что эта связь перекрывается с sap_request_failed
    )
    kaspi_payment_failed: Mapped[List["KaspiPaymentModel"]] = relationship(
        "KaspiPaymentModel",
        back_populates="order_failed",
        foreign_keys="[KaspiPaymentModel.order_id]",
        uselist=True,
        primaryjoin="and_(KaspiPaymentModel.order_id == OrderModel.id, KaspiPaymentModel.is_paid == False)",
        overlaps="kaspi_payment",  # Указываем, что эта связь перекрывается с sap_request
        viewonly=True
    )
