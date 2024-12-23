from datetime import datetime

from sqlalchemy import ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.shared.database_constants import ID, AppTableNames, CreatedAt, UpdatedAt, TableConstantsNames


class InitialWeightModel(Base):
    __tablename__ = AppTableNames.InitialWeightTableName
    id: Mapped[ID]

    history_id: Mapped[int | None] = mapped_column(
        ForeignKey(
            AppTableNames.ScheduleHistoryTableName + ".id",
            onupdate="cascade",
            ondelete="set null",
        ),
        nullable=True,
    )

    order_id: Mapped[int | None] = mapped_column(
        ForeignKey(
            AppTableNames.OrderTableName + ".id", onupdate="cascade", ondelete="set null"
        ),
        nullable=True,
    )

    zakaz: Mapped[str] = mapped_column(String(length=20), index=True, nullable=True)

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

    responsible_id: Mapped[int | None] = mapped_column(
        ForeignKey(
            AppTableNames.UserTableName + ".id", onupdate="cascade", ondelete="set null"
        ),
        nullable=True,
    )
    responsible_name: Mapped[str] = mapped_column(String(TableConstantsNames.STANDARD_LENGTH_STRING), nullable=True)
    responsible_iin: Mapped[str] = mapped_column(String(TableConstantsNames.STANDARD_LENGTH_STRING), nullable=True)

    vehicle_tara_kg: Mapped[int] = mapped_column(Integer())
    measured_at: Mapped[datetime] = mapped_column()

    created_at: Mapped[CreatedAt]
    updated_at: Mapped[UpdatedAt]

    history: Mapped["ScheduleHistoryModel"] = relationship(
        "ScheduleHistoryModel",
        back_populates="initial_weights",
        foreign_keys=[history_id],
    )

    order: Mapped["OrderModel"] = relationship(
        "OrderModel", back_populates="initial_weights", foreign_keys=[order_id]
    )

    vehicle: Mapped["VehicleModel"] = relationship(
        "VehicleModel",
        back_populates="initial_weights_vehicle",
        foreign_keys=[vehicle_id],
    )

    trailer: Mapped["VehicleModel"] = relationship(
        "VehicleModel",
        back_populates="initial_weights_trailer",
        foreign_keys=[trailer_id],
    )

    responsible: Mapped["UserModel"] = relationship(
        "UserModel", back_populates="initial_weights", foreign_keys=[responsible_id]
    )
