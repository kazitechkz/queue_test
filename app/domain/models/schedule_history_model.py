from datetime import datetime
from typing import Optional

from sqlalchemy import ForeignKey, Text, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base

from app.shared.database_constants import AppTableNames, ID, CreatedAt, UpdatedAt


class ScheduleHistoryModel(Base):
    __tablename__ = AppTableNames.ScheduleHistoryTableName
    id: Mapped[ID]
    schedule_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey(AppTableNames.ScheduleTableName + ".id", onupdate="cascade", ondelete="set null"), nullable=True)
    operation_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey(AppTableNames.OperationTableName + ".id", onupdate="cascade", ondelete="set null"), nullable=True)
    responsible_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey(AppTableNames.UserTableName + ".id", onupdate="cascade", ondelete="set null"), nullable=True)
    responsible_name: Mapped[str] = mapped_column(String(256), nullable=True)
    responsible_iin: Mapped[str] = mapped_column(String(256), nullable=True)

    is_passed: Mapped[Optional[bool]] = mapped_column(nullable=True)
    start_at: Mapped[datetime] = mapped_column(nullable=True)
    end_at: Mapped[datetime] = mapped_column(nullable=True)
    canceled_at: Mapped[Optional[datetime]] = mapped_column(nullable=True)
    cancel_reason: Mapped[str] = mapped_column(Text(length=1000), nullable=True)
    created_at: Mapped[CreatedAt]
    updated_at: Mapped[UpdatedAt]

    schedule: Mapped["ScheduleModel"] = relationship("ScheduleModel")
    operation: Mapped["OperationModel"] = relationship("OperationModel")

    act_weights:Mapped[list["ActWeightModel"]] = relationship(
        "ActWeightModel",
        back_populates="history",
        foreign_keys="[ActWeightModel.history_id]"
    )

    initial_weights:Mapped[list["InitialWeightModel"]] = relationship(
        "InitialWeightModel",
        back_populates="history",
        foreign_keys="[InitialWeightModel.history_id]"
    )