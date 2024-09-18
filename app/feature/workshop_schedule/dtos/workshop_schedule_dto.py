from datetime import datetime, date, time
from typing import Optional

from pydantic import BaseModel, Field


class WorkshopScheduleDTO(BaseModel):
    id: int
    created_at: datetime = Field(..., description="Дата создания")
    updated_at: datetime = Field(..., description="Дата последнего обновления")

    class Config:
        from_attributes = True

class WorkshopScheduleRDTO(WorkshopScheduleDTO):
    workshop_id: Optional[int] = Field(None, description="ID мастерской")
    workshop_sap_id: str = Field(..., max_length=256, description="SAP ID мастерской")
    date_start: date = Field(..., description="Дата начала")
    date_end: date = Field(..., description="Дата окончания")
    start_at: time = Field(..., description="Время начала работы")
    end_at: time = Field(..., description="Время окончания работы")
    car_service_min: int = Field(..., description="Минимальное время обслуживания машины (мин)")
    break_between_service_min: int = Field(..., description="Перерыв между обслуживанием машин (мин)")
    machine_at_one_time: int = Field(..., description="Количество машин одновременно")
    is_active: bool = Field(..., description="Активен ли график")

class WorkshopScheduleСDTO(BaseModel):
    workshop_id: Optional[int] = Field(None, description="ID мастерской")
    workshop_sap_id: str = Field(..., max_length=256, description="SAP ID мастерской")
    date_start: date = Field(..., description="Дата начала")
    date_end: date = Field(..., description="Дата окончания")
    start_at: time = Field(..., description="Время начала работы")
    end_at: time = Field(..., description="Время окончания работы")
    car_service_min: int = Field(..., description="Минимальное время обслуживания машины (мин)")
    break_between_service_min: int = Field(..., description="Перерыв между обслуживанием машин (мин)")
    machine_at_one_time: int = Field(..., description="Количество машин одновременно")
    is_active: bool = Field(..., description="Активен ли график")

