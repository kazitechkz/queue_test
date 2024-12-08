from datetime import date, time

from sqlalchemy import Boolean, Date, ForeignKey, Integer, String, Time
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.domain.models.workshop_model import WorkshopModel
from app.shared.database_constants import ID, AppTableNames, CreatedAt, UpdatedAt, TableConstantsNames


class WorkshopScheduleModel(Base):
    __tablename__ = AppTableNames.WorkshopScheduleTableName
    id: Mapped[ID]
    workshop_id: Mapped[int] = mapped_column(
        ForeignKey(
            AppTableNames.WorkshopTableName + ".id",
            ondelete="set null",
            onupdate="cascade",
        ),
        nullable=True,
    )
    workshop_sap_id: Mapped[str] = mapped_column(String(length=TableConstantsNames.STANDARD_LENGTH_STRING), index=True)
    date_start: Mapped[date] = mapped_column(Date())
    date_end: Mapped[date] = mapped_column(Date())
    start_at: Mapped[time] = mapped_column(Time())
    end_at: Mapped[time] = mapped_column(Time())
    car_service_min: Mapped[int] = mapped_column(Integer())
    break_between_service_min: Mapped[int] = mapped_column(Integer())
    machine_at_one_time: Mapped[int] = mapped_column(Integer())
    is_active: Mapped[bool] = mapped_column(Boolean())
    created_at: Mapped[CreatedAt]
    updated_at: Mapped[UpdatedAt]

    workshop: Mapped[WorkshopModel] = relationship("WorkshopModel")
