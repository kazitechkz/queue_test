from datetime import datetime

from sqlalchemy import Boolean, Computed, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.shared.database_constants import ID, AppTableNames, CreatedAt, UpdatedAt, TableConstantsNames


class ScheduleModel(Base):
    __tablename__ = AppTableNames.ScheduleTableName
    id: Mapped[ID]

    order_id: Mapped[int | None] = mapped_column(
        ForeignKey(
            AppTableNames.OrderTableName + ".id", onupdate="cascade", ondelete="set null"
        ),
        nullable=True,
    )
    zakaz: Mapped[str] = mapped_column(String(length=TableConstantsNames.SAP_ORDER_LENGTH_STRING), index=True, nullable=True)

    owner_id: Mapped[int | None] = mapped_column(
        ForeignKey(
            AppTableNames.UserTableName + ".id", onupdate="cascade", ondelete="set null"
        ),
        nullable=True,
    )
    owner_name: Mapped[str] = mapped_column(String(TableConstantsNames.STANDARD_LENGTH_STRING))
    owner_iin: Mapped[str] = mapped_column(String(TableConstantsNames.STANDARD_LENGTH_STRING))

    driver_id: Mapped[int | None] = mapped_column(
        ForeignKey(
            AppTableNames.UserTableName + ".id", onupdate="cascade", ondelete="set null"
        ),
        nullable=True,
    )
    driver_name: Mapped[str] = mapped_column(String(TableConstantsNames.STANDARD_LENGTH_STRING))
    driver_iin: Mapped[str] = mapped_column(String(TableConstantsNames.STANDARD_LENGTH_STRING))

    organization_id: Mapped[int | None] = mapped_column(
        ForeignKey(
            AppTableNames.OrganizationTableName + ".id",
            onupdate="cascade",
            ondelete="set null",
        ),
        nullable=True,
    )
    organization_full_name: Mapped[str] = mapped_column(String(TableConstantsNames.STANDARD_LENGTH_STRING), nullable=True)
    organization_bin: Mapped[str] = mapped_column(String(TableConstantsNames.STANDARD_LENGTH_STRING), nullable=True)

    vehicle_id: Mapped[int | None] = mapped_column(
        ForeignKey(
            AppTableNames.VehicleTableName + ".id",
            onupdate="cascade",
            ondelete="set null",
        ),
        nullable=True,
    )
    vehicle_info: Mapped[str] = mapped_column(Text())

    trailer_id: Mapped[int | None] = mapped_column(
        ForeignKey(
            AppTableNames.VehicleTableName + ".id",
            onupdate="cascade",
            ondelete="set null",
        ),
        nullable=True,
    )
    trailer_info: Mapped[str | None] = mapped_column(Text(), nullable=True)

    workshop_schedule_id: Mapped[int | None] = mapped_column(
        ForeignKey(
            AppTableNames.WorkshopScheduleTableName + ".id",
            onupdate="cascade",
            ondelete="set null",
        ),
        nullable=True,
    )

    current_operation_id: Mapped[int | None] = mapped_column(
        ForeignKey(
            AppTableNames.OperationTableName + ".id",
            onupdate="cascade",
            ondelete="set null",
        ),
        nullable=True,
    )

    start_at: Mapped[datetime] = mapped_column()
    end_at: Mapped[datetime] = mapped_column()

    rescheduled_start_at: Mapped[datetime | None] = mapped_column()
    rescheduled_end_at: Mapped[datetime | None] = mapped_column()

    loading_volume_kg: Mapped[int] = mapped_column(Integer())
    vehicle_tara_kg: Mapped[int] = mapped_column(Integer(), nullable=True)
    vehicle_brutto_kg: Mapped[int] = mapped_column(Integer(), nullable=True)
    vehicle_netto_kg: Mapped[int] = mapped_column(
        Computed("vehicle_brutto_kg - vehicle_tara_kg"), nullable=True
    )

    responsible_id: Mapped[int | None] = mapped_column(
        ForeignKey(
            AppTableNames.UserTableName + ".id", onupdate="cascade", ondelete="set null"
        ),
        nullable=True,
    )
    responsible_name: Mapped[str] = mapped_column(String(TableConstantsNames.STANDARD_LENGTH_STRING), nullable=True)

    is_active: Mapped[bool] = mapped_column(Boolean(), default=True)
    is_used: Mapped[bool] = mapped_column(Boolean(), default=False)
    is_canceled: Mapped[bool] = mapped_column(Boolean(), default=False)
    is_executed: Mapped[bool] = mapped_column(Boolean(), default=False)
    executed_at: Mapped[datetime | None] = mapped_column(nullable=True)

    canceled_by: Mapped[int | None] = mapped_column(
        ForeignKey(
            AppTableNames.UserTableName + ".id", onupdate="cascade", ondelete="set null"
        ),
        nullable=True,
    )
    cancel_reason: Mapped[str] = mapped_column(Text(), nullable=True)
    canceled_at: Mapped[datetime | None] = mapped_column(nullable=True)

    created_at: Mapped[CreatedAt]
    updated_at: Mapped[UpdatedAt]

    workshop_schedule: Mapped["WorkshopScheduleModel"] = relationship(
        "WorkshopScheduleModel", foreign_keys=[workshop_schedule_id]
    )
    current_operation: Mapped["OperationModel"] = relationship(
        "OperationModel", foreign_keys=[current_operation_id]
    )
    vehicle: Mapped["VehicleModel"] = relationship(
        "VehicleModel", foreign_keys=[vehicle_id]
    )
    trailer: Mapped["VehicleModel"] = relationship(
        "VehicleModel", foreign_keys=[trailer_id]
    )
    order: Mapped["OrderModel"] = relationship("OrderModel", foreign_keys=[order_id])
    owner: Mapped["UserModel"] = relationship("UserModel", foreign_keys=[owner_id])
    driver: Mapped["UserModel"] = relationship("UserModel", foreign_keys=[driver_id])
    organization: Mapped["OrganizationModel"] = relationship(
        "OrganizationModel", foreign_keys=[organization_id]
    )
    responsible: Mapped["UserModel"] = relationship(
        "UserModel", foreign_keys=[responsible_id]
    )
    canceled_user: Mapped["UserModel"] = relationship(
        "UserModel", foreign_keys=[canceled_by]
    )
    schedule_histories: Mapped[list["ScheduleHistoryModel"]] = relationship(
        "ScheduleHistoryModel", foreign_keys="[ScheduleHistoryModel.schedule_id]"
    )
