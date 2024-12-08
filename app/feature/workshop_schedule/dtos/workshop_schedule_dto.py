from datetime import date, datetime, time

from pydantic import BaseModel, Field, model_validator

from app.feature.factory.dtos.factory_dto import FactoryRDTO
from app.feature.material.dtos.material_dto import MaterialRDTO
from app.shared.database_constants import TableConstantsNames


class WorkshopScheduleDTO(BaseModel):
    id: int
    created_at: datetime = Field(..., description="Дата создания")
    updated_at: datetime = Field(..., description="Дата последнего обновления")

    class Config:
        from_attributes = True


class WorkshopScheduleRDTO(WorkshopScheduleDTO):
    workshop_id: int | None = Field(None, description="ID мастерской")
    workshop_sap_id: str = Field(..., max_length=TableConstantsNames.STANDARD_LENGTH_STRING, description="SAP ID мастерской")
    date_start: date = Field(..., description="Дата начала")
    date_end: date = Field(..., description="Дата окончания")
    start_at: time = Field(..., description="Время начала работы")
    end_at: time = Field(..., description="Время окончания работы")
    car_service_min: int = Field(
        ..., description="Минимальное время обслуживания машины (мин)"
    )
    break_between_service_min: int = Field(
        ..., description="Перерыв между обслуживанием машин (мин)"
    )
    machine_at_one_time: int = Field(..., description="Количество машин одновременно")
    is_active: bool = Field(..., description="Активен ли график")

    class Config:
        from_attributes = True


class WorkshopScheduleCDTO(BaseModel):
    workshop_id: int | None = Field(None, description="ID мастерской")
    workshop_sap_id: str = Field(..., max_length=TableConstantsNames.STANDARD_LENGTH_STRING, description="SAP ID мастерской")
    date_start: date = Field(..., description="Дата начала")
    date_end: date = Field(..., description="Дата окончания")
    start_at: time = Field(..., description="Время начала работы")
    end_at: time = Field(..., description="Время окончания работы")
    car_service_min: int = Field(
        ..., ge=0, description="Минимальное время обслуживания машины (мин)"
    )
    break_between_service_min: int = Field(
        ..., ge=0, description="Перерыв между обслуживанием машин (мин)"
    )
    machine_at_one_time: int = Field(
        ..., gt=0, description="Количество машин одновременно"
    )
    is_active: bool = Field(..., description="Активен ли график")

    @model_validator(mode="before")
    def check_dates_and_times(self, values):
        date_start = values.get("date_start")
        date_end = values.get("date_end")
        start_at = values.get("start_at")
        end_at = values.get("end_at")

        # Проверка, что дата окончания больше даты начала
        if date_start and date_end and date_end <= date_start:
            msg = "Дата окнчания должна быть больше даты начала"
            raise ValueError(msg)

        # Проверка, что время окончания больше времени начала
        if start_at and end_at and end_at <= start_at:
            msg = "Время окончания работы должна быть больше даты начала"
            raise ValueError(msg)

        return values

    class Config:
        from_attributes = True


class WorkshopScheduleWithRelationsRDTO(WorkshopScheduleRDTO):
    factory: FactoryRDTO | None
    materials: list[MaterialRDTO] | None

    class Config:
        from_attributes = True
