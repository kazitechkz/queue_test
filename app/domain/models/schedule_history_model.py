from datetime import datetime

from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.shared.database_constants import ID, AppTableNames, CreatedAt, UpdatedAt, TableConstantsNames


class ScheduleHistoryModel(Base):
    __tablename__ = AppTableNames.ScheduleHistoryTableName
    id: Mapped[ID]
    schedule_id: Mapped[int | None] = mapped_column(
        ForeignKey(
            AppTableNames.ScheduleTableName + ".id",
            onupdate="cascade",
            ondelete="set null",
        ),
        nullable=True,
    )
    operation_id: Mapped[int | None] = mapped_column(
        ForeignKey(
            AppTableNames.OperationTableName + ".id",
            onupdate="cascade",
            ondelete="set null",
        ),
        nullable=True,
    )
    responsible_id: Mapped[int | None] = mapped_column(
        ForeignKey(
            AppTableNames.UserTableName + ".id", onupdate="cascade", ondelete="set null"
        ),
        nullable=True,
    )
    responsible_name: Mapped[str] = mapped_column(String(TableConstantsNames.STANDARD_LENGTH_STRING), nullable=True)
    responsible_iin: Mapped[str] = mapped_column(String(TableConstantsNames.STANDARD_LENGTH_STRING), nullable=True)

    is_passed: Mapped[bool | None] = mapped_column(nullable=True)
    start_at: Mapped[datetime] = mapped_column(nullable=True)
    end_at: Mapped[datetime] = mapped_column(nullable=True)
    canceled_at: Mapped[datetime | None] = mapped_column(nullable=True)
    cancel_reason: Mapped[str] = mapped_column(Text(), nullable=True)
    created_at: Mapped[CreatedAt]
    updated_at: Mapped[UpdatedAt]

    schedule: Mapped["ScheduleModel"] = relationship("ScheduleModel")
    operation: Mapped["OperationModel"] = relationship("OperationModel")

    act_weights: Mapped["ActWeightModel"] = relationship(
        "ActWeightModel",
        back_populates="history",
        foreign_keys="[ActWeightModel.history_id]",
        uselist=False,
    )

    initial_weights: Mapped["InitialWeightModel"] = relationship(
        "InitialWeightModel",
        back_populates="history",
        foreign_keys="[InitialWeightModel.history_id]",
        uselist=False,
    )
