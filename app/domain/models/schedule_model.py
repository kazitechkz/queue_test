from datetime import datetime
from typing import Optional

from sqlalchemy import ForeignKey, Integer, Boolean, Text, String, Computed
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base

from app.shared.database_constants import AppTableNames, CreatedAt, UpdatedAt, ID


class ScheduleModel(Base):
    __tablename__ = AppTableNames.ScheduleTableName
    id: Mapped[ID]

    order_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey(AppTableNames.OrderTableName + ".id", onupdate="cascade", ondelete="set null"), nullable=True)
    zakaz: Mapped[str] = mapped_column(String(length=20), index=True, nullable=True)

    owner_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey(AppTableNames.UserTableName + ".id", onupdate="cascade", ondelete="set null"), nullable=True)
    owner_name: Mapped[str] = mapped_column(String(256))
    owner_iin: Mapped[str] = mapped_column(String(256))

    driver_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey(AppTableNames.UserTableName + ".id", onupdate="cascade", ondelete="set null"), nullable=True)
    driver_name: Mapped[str] = mapped_column(String(256))
    driver_iin: Mapped[str] = mapped_column(String(256))

    organization_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey(AppTableNames.OrganizationTableName + ".id", onupdate="cascade", ondelete="set null"), nullable=True)
    organization_full_name: Mapped[str] = mapped_column(String(256), nullable=True)
    organization_bin: Mapped[str] = mapped_column(String(256), nullable=True)

    vehicle_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey(AppTableNames.VehicleTableName + ".id", onupdate="cascade", ondelete="set null"), nullable=True)
    vehicle_info: Mapped[str] = mapped_column(Text(length=1000))

    trailer_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey(AppTableNames.VehicleTableName + ".id", onupdate="cascade", ondelete="set null"), nullable=True)
    trailer_info: Mapped[Optional[str]] = mapped_column(Text(length=1000), nullable=True)

    workshop_schedule_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey(AppTableNames.WorkshopScheduleTableName + ".id", onupdate="cascade", ondelete="set null"),
        nullable=True)

    current_operation_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey(AppTableNames.OperationTableName + ".id", onupdate="cascade", ondelete="set null"), nullable=True)

    start_at: Mapped[datetime] = mapped_column()
    end_at: Mapped[datetime] = mapped_column()

    loading_volume_kg: Mapped[int] = mapped_column(Integer())
    vehicle_tara_kg: Mapped[int] = mapped_column(Integer(), nullable=True)
    vehicle_brutto_kg: Mapped[int] = mapped_column(Integer(), nullable=True)
    vehicle_netto_kg: Mapped[int] = mapped_column(Computed("vehicle_brutto_kg - vehicle_tara_kg"), nullable=True)

    responsible_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey(AppTableNames.UserTableName + ".id", onupdate="cascade", ondelete="set null"), nullable=True)
    responsible_name: Mapped[str] = mapped_column(String(256), nullable=True)

    is_active: Mapped[bool] = mapped_column(Boolean(), default=True)
    is_used: Mapped[bool] = mapped_column(Boolean(), default=False)
    is_canceled: Mapped[bool] = mapped_column(Boolean(), default=False)
    is_executed: Mapped[bool] = mapped_column(Boolean(), default=False)
    executed_at: Mapped[Optional[datetime]] = mapped_column(nullable=True)

    canceled_by: Mapped[Optional[int]] = mapped_column(
        ForeignKey(AppTableNames.UserTableName + ".id", onupdate="cascade", ondelete="set null"), nullable=True)
    cancel_reason: Mapped[str] = mapped_column(Text(length=1000), nullable=True)
    canceled_at: Mapped[Optional[datetime]] = mapped_column(nullable=True)

    created_at: Mapped[CreatedAt]
    updated_at: Mapped[UpdatedAt]

    workshop_schedule: Mapped["WorkshopScheduleModel"] = relationship("WorkshopScheduleModel", foreign_keys=[workshop_schedule_id])
    current_operation: Mapped["OperationModel"] = relationship("OperationModel", foreign_keys=[current_operation_id])
    vehicle: Mapped["VehicleModel"] = relationship("VehicleModel", foreign_keys=[vehicle_id])
    order: Mapped["OrderModel"] = relationship("OrderModel", foreign_keys=[order_id])
