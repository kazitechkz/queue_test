from datetime import date, datetime, time

from pydantic import BaseModel, Field, model_validator

from app.feature.operation.dtos.operation_dto import OperationRDTO
from app.shared.database_constants import TableConstantsNames


class ScheduleDTO(BaseModel):
    id: int

    created_at: datetime = Field(..., description="Дата создания")
    updated_at: datetime = Field(..., description="Дата последнего обновления")

    class Config:
        from_attributes = True


class ScheduleRDTO(ScheduleDTO):
    order_id: int | None = Field(None, description="ID заказа")
    zakaz: str | None = Field(None, max_length=TableConstantsNames.SAP_ORDER_LENGTH_STRING, description="Заказ")

    owner_id: int | None = Field(None, description="ID владельца")
    owner_name: str = Field(..., max_length=TableConstantsNames.STANDARD_LENGTH_STRING, description="Имя владельца")
    owner_iin: str = Field(..., max_length=TableConstantsNames.STANDARD_LENGTH_STRING, description="ИИН владельца")

    driver_id: int | None = Field(None, description="ID водителя")
    driver_name: str = Field(..., max_length=TableConstantsNames.STANDARD_LENGTH_STRING, description="Имя водителя")
    driver_iin: str = Field(..., max_length=TableConstantsNames.STANDARD_LENGTH_STRING, description="ИИН водителя")

    organization_id: int | None = Field(None, description="ID организации")
    organization_full_name: str | None = Field(
        None, max_length=TableConstantsNames.STANDARD_LENGTH_STRING, description="Полное название организации"
    )
    organization_bin: str | None = Field(
        None, max_length=TableConstantsNames.STANDARD_LENGTH_STRING, description="БИН организации"
    )

    vehicle_id: int | None = Field(None, description="ID транспортного средства")
    vehicle_info: str = Field(
        ..., max_length=TableConstantsNames.STANDARD_TEXT_LENGTH_MAX, description="Информация о транспортном средстве"
    )

    trailer_id: int | None = Field(None, description="ID прицепа")
    trailer_info: str | None = Field(
        None, max_length=TableConstantsNames.STANDARD_TEXT_LENGTH_MAX, description="Информация о прицепе"
    )

    workshop_schedule_id: int | None = Field(None, description="ID расписания мастерской")
    current_operation_id: int | None = Field(None, description="Текущая операция")

    start_at: datetime = Field(..., description="Время начала")
    end_at: datetime = Field(..., description="Время окончания")

    rescheduled_start_at: datetime | None = Field(
        default=None, description="Время начала перенос"
    )
    rescheduled_end_at: datetime | None = Field(
        default=None, description="Время окончания перенос"
    )

    loading_volume_kg: int = Field(..., description="Объем загрузки в кг")
    vehicle_tara_kg: int | None = Field(
        None, description="Тара транспортного средства в кг"
    )
    vehicle_brutto_kg: int | None = Field(
        None, description="Брутто транспортного средства в кг"
    )
    vehicle_netto_kg: int | None = Field(
        None, description="Нетто транспортного средства в кг"
    )

    responsible_id: int | None = Field(None, description="ID ответственного")
    responsible_name: str | None = Field(
        None, max_length=TableConstantsNames.STANDARD_LENGTH_STRING, description="Имя ответственного"
    )

    is_active: bool = Field(..., description="Активно ли расписание")
    is_used: bool = Field(..., description="Использовано ли расписание")
    is_canceled: bool = Field(..., description="Отменено ли расписание")
    is_executed: bool = Field(..., description="Выполнено ли расписание")
    executed_at: datetime | None = Field(None, description="Время выполнения")

    canceled_by: int | None = Field(None, description="Кто отменил")
    cancel_reason: str | None = Field(None, max_length=TableConstantsNames.STANDARD_TEXT_LENGTH_MAX, description="Причина отмены")
    canceled_at: datetime | None = Field(None, description="Время отмены")

    current_operation: OperationRDTO

    class Config:
        from_attributes = True


class ScheduleCDTO(BaseModel):
    order_id: int | None = Field(None, description="ID заказа")
    zakaz: str | None = Field(None, max_length=TableConstantsNames.SAP_ORDER_LENGTH_STRING, description="Заказ")

    owner_id: int | None = Field(None, description="ID владельца")
    owner_name: str = Field(..., max_length=TableConstantsNames.STANDARD_LENGTH_STRING, description="Имя владельца")
    owner_iin: str = Field(..., max_length=TableConstantsNames.STANDARD_LENGTH_STRING, description="ИИН владельца")

    driver_id: int | None = Field(None, description="ID водителя")
    driver_name: str = Field(..., max_length=TableConstantsNames.STANDARD_LENGTH_STRING, description="Имя водителя")
    driver_iin: str = Field(..., max_length=TableConstantsNames.STANDARD_LENGTH_STRING, description="ИИН водителя")

    organization_id: int | None = Field(None, description="ID организации")
    organization_full_name: str | None = Field(
        None, max_length=TableConstantsNames.STANDARD_LENGTH_STRING, description="Полное название организации"
    )
    organization_bin: str | None = Field(
        None, max_length=TableConstantsNames.STANDARD_LENGTH_STRING, description="БИН организации"
    )

    vehicle_id: int | None = Field(None, description="ID транспортного средства")
    vehicle_info: str = Field(
        ..., max_length=TableConstantsNames.STANDARD_TEXT_LENGTH_MAX, description="Информация о транспортном средстве"
    )

    trailer_id: int | None = Field(None, description="ID прицепа")
    trailer_info: str | None = Field(
        None, max_length=TableConstantsNames.STANDARD_TEXT_LENGTH_MAX, description="Информация о прицепе"
    )

    workshop_schedule_id: int | None = Field(None, description="ID расписания мастерской")
    current_operation_id: int | None = Field(None, description="Текущая операция")

    start_at: datetime = Field(..., description="Время начала")
    end_at: datetime = Field(..., description="Время окончания")

    rescheduled_start_at: datetime | None = Field(
        default=None, description="Время начала перенос"
    )
    rescheduled_end_at: datetime | None = Field(
        default=None, description="Время окончания перенос"
    )

    loading_volume_kg: int = Field(..., description="Объем загрузки в кг")
    vehicle_tara_kg: int | None = Field(
        None, description="Тара транспортного средства в кг"
    )
    vehicle_brutto_kg: int | None = Field(
        None, description="Брутто транспортного средства в кг"
    )
    vehicle_netto_kg: int | None = Field(
        None, description="Нетто транспортного средства в кг"
    )

    responsible_id: int | None = Field(None, description="ID ответственного")
    responsible_name: str | None = Field(
        None, max_length=TableConstantsNames.STANDARD_LENGTH_STRING, description="Имя ответственного"
    )

    is_active: bool | None = Field(True, description="Активно ли расписание")
    is_used: bool | None = Field(False, description="Использовано ли расписание")
    is_canceled: bool | None = Field(False, description="Отменено ли расписание")
    is_executed: bool | None = Field(False, description="Выполнено ли расписание")
    executed_at: datetime | None = Field(None, description="Время выполнения")

    canceled_by: int | None = Field(None, description="Кто отменил")
    cancel_reason: str | None = Field(None, max_length=TableConstantsNames.STANDARD_TEXT_LENGTH_MAX, description="Причина отмены")
    canceled_at: datetime | None = Field(None, description="Время отмены")

    @model_validator(mode="after")
    def check_dates_and_times(self):
        start_at = self.start_at
        end_at = self.end_at
        if start_at and end_at and end_at <= start_at:
            msg = "Время окончания работы должна быть больше даты начала"
            raise ValueError(msg)
        return self

    class Config:
        from_attributes = True


class ScheduleIndividualCDTO(BaseModel):
    order_id: int = Field(description="ID заказа")
    workshop_schedule_id: int = Field(description="Шаблон расписания цеха")
    scheduled_data: date = Field(description="Дата бронирования", ge=date.today())
    start_at: time = Field(description="Начало бронирования")
    end_at: time = Field(description="Конец бронирования")
    vehicle_id: int | None = Field(None, description="ID транспортного средства")
    trailer_id: int | None = Field(None, description="ID прицепа")
    booked_quan_t: float = Field(description="Общая масса бронирования в тоннах", ge=1)

    @model_validator(mode="after")
    def check_dates_and_times(self):
        start_at = self.start_at
        end_at = self.end_at
        if start_at and end_at and end_at <= start_at:
            msg = "Время окончания работы должна быть больше даты начала"
            raise ValueError(msg)
        return self


class ScheduleLegalCDTO(BaseModel):
    organization_id: int = Field(description="ID организации")
    order_id: int = Field(description="ID заказа")
    driver_id: int = (Field(description="ID водителя"),)
    workshop_schedule_id: int = Field(description="Шаблон расписания цеха")
    scheduled_data: date = Field(description="Дата бронирования", ge=date.today())
    start_at: time = Field(description="Начало бронирования")
    end_at: time = Field(description="Конец бронирования")
    vehicle_id: int | None = Field(None, description="ID транспортного средства")
    trailer_id: int | None = Field(None, description="ID прицепа")
    booked_quan_t: float = Field(description="Общая масса бронирования в тоннах")

    @model_validator(mode="after")
    def check_dates_and_times(self):
        start_at = self.start_at
        end_at = self.end_at
        if start_at and end_at and end_at <= start_at:
            msg = "Время окончания работы должна быть больше даты начала"
            raise ValueError(msg)
        return self

    @model_validator(mode="before")
    def validate_scheduled_data(cls, values: dict) -> dict:
        scheduled_data = values.get("scheduled_data")
        if scheduled_data and scheduled_data < date.today():
            raise ValueError("Время начала работы должна быть больше чем текущее")
        return values

    class Config:
        from_attributes = True


class ScheduleSpaceDTO(BaseModel):
    workshop_schedule_id: int = Field(description="Уникальный идентификатор бронирования")
    scheduled_data: date = Field(description="Дата бронирования", ge=date.today())
    start_at: time = Field(description="Начало бронирования")
    end_at: time = Field(description="Конец бронирования")
    free_space: int = Field(
        title="Кол-во свободных мест", description="Кол-во свободных мест"
    )


class ScheduleCalendarDTO(BaseModel):
    scheduled_at: date = Field(description="Дата бронирования")
    total: int = Field(description="Общее количество бронирований")
    total_active: int = Field(description="Общее количество активных бронирований")
    total_canceled: int = Field(description="Количество отменненых бронирований")
    total_executed: int = Field(description="Количество выполненых бронирований")


class RescheduleAllDTO(BaseModel):
    scheduled_data: date = Field(description="Дата бронирования", ge=date.today())
    minute: int = Field(description="Перенос в минутах", gt=0, le=120)


class ScheduleCancelDTO(BaseModel):
    scheduled_data: date = Field(description="Дата бронирования", ge=date.today())
    cancel_reason: str | None = Field(None, max_length=TableConstantsNames.STANDARD_TEXT_LENGTH_MAX, description="Причина отмены")


class RescheduleOneDTO(BaseModel):
    scheduled_data: date = Field(description="Дата бронирования", ge=date.today())
    start_at: time = Field(description="Начало бронирования")
    end_at: time = Field(description="Конец бронирования")

    @model_validator(mode="after")
    def check_dates_and_times(self):
        start_at = self.start_at
        end_at = self.end_at
        if start_at and end_at and end_at <= start_at:
            msg = "Время окончания работы должна быть больше даты начала"
            raise ValueError(msg)
        return self


class ScheduleCancelOneDTO(BaseModel):
    cancel_reason: str | None = Field(None, max_length=TableConstantsNames.STANDARD_TEXT_LENGTH_MAX, description="Причина отмены")


class ScheduleRDTOWithRelation(ScheduleRDTO):
    current_operation: OperationRDTO | None = None
    # order: Optional[OrderRDTO] = None
    # pass
