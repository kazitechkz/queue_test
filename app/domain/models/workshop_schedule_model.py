from datetime import date, time

from sqlalchemy import ForeignKey, String, Date, Time, Integer, Boolean
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base
from app.shared.database_constants import AppTableNames, ID, UpdatedAt, CreatedAt


class WorkshopScheduleModel(Base):
    __tablename__ = AppTableNames.WorkshopScheduleTableName
    id: Mapped[ID]
    workshop_id: Mapped[int] = mapped_column(
        ForeignKey(AppTableNames.WorkshopTableName + ".id", ondelete="set null", onupdate="cascade"), nullable=True)
    workshop_sap_id: Mapped[str] = mapped_column(String(length=256), index=True)
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
