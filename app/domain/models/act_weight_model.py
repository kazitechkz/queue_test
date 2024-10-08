from datetime import datetime
from typing import Optional

from sqlalchemy import ForeignKey, String, Integer, Computed, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.shared.database_constants import AppTableNames, ID, CreatedAt, UpdatedAt


class ActWeightModel(Base):
    __tablename__ = AppTableNames.ActWeightTableName
    id: Mapped[ID]

    history_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey(AppTableNames.ScheduleHistoryTableName + ".id", onupdate="cascade", ondelete="set null"),
        nullable=True)

    order_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey(AppTableNames.OrderTableName + ".id", onupdate="cascade", ondelete="set null"), nullable=True)
    zakaz: Mapped[str] = mapped_column(String(length=20), index=True, nullable=True)

    vehicle_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey(AppTableNames.VehicleTableName + ".id", onupdate="cascade", ondelete="set null"), nullable=True)
    vehicle_info: Mapped[str] = mapped_column(Text(length=1000))

    trailer_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey(AppTableNames.VehicleTableName + ".id", onupdate="cascade", ondelete="set null"), nullable=True)
    trailer_info: Mapped[Optional[str]] = mapped_column(Text(length=1000), nullable=True)

    responsible_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey(AppTableNames.UserTableName + ".id", onupdate="cascade", ondelete="set null"), nullable=True)
    responsible_name: Mapped[str] = mapped_column(String(256), nullable=True)
    responsible_iin: Mapped[str] = mapped_column(String(256), nullable=True)

    vehicle_tara_kg: Mapped[int] = mapped_column(Integer())
    vehicle_netto_kg: Mapped[int] = mapped_column(Computed("vehicle_brutto_kg - vehicle_tara_kg"))
    vehicle_brutto_kg: Mapped[int] = mapped_column(Integer())

    measured_at: Mapped[datetime] = mapped_column()
    created_at: Mapped[CreatedAt]
    updated_at: Mapped[UpdatedAt]

    history:Mapped["ScheduleHistoryModel"] = relationship(
        "ScheduleHistoryModel",
        back_populates="act_weights",
        foreign_keys=[history_id]
    )

    order:Mapped["OrderModel"] = relationship(
        "OrderModel",
        back_populates="act_weights",
        foreign_keys=[order_id]
    )

    responsible:Mapped["UserModel"] = relationship(
        "UserModel",
        back_populates="act_weights",
        foreign_keys=[responsible_id]
    )

    vehicle: Mapped["VehicleModel"] = relationship(
        "VehicleModel",
        back_populates="act_weights_vehicle",
        foreign_keys=[vehicle_id]
    )

    trailer: Mapped["VehicleModel"] = relationship(
        "VehicleModel",
        back_populates="act_weights_trailer",
        foreign_keys=[trailer_id]
    )