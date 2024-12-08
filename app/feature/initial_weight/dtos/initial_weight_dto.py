from datetime import datetime

from pydantic import BaseModel, Field

from app.feature.order.dtos.order_dto import OrderRDTO
from app.feature.schedule_history.dtos.schedule_history_dto import ScheduleHistoryRDTO
from app.feature.user.dtos.user_dto import UserRDTO
from app.feature.vehicle.dtos.vehicle_dto import VehicleRDTO
from app.shared.database_constants import TableConstantsNames


class InitialWeightDTO(BaseModel):
    id: int = Field(..., description="Уникальный идентификатор")

    created_at: datetime = Field(..., description="Дата и время создания")
    updated_at: datetime = Field(..., description="Дата и время последнего обновления")

    class Config:
        from_attributes = True


class InitialWeightRDTO(InitialWeightDTO):
    history_id: int | None = Field(None, description="ID истории")
    order_id: int | None = Field(None, description="ID заказа")

    zakaz: str | None = Field(None, description="Номер заказа", max_length=TableConstantsNames.SAP_ORDER_LENGTH_STRING)

    vehicle_id: int | None = Field(None, description="ID транспортного средства")
    vehicle_info: str = Field(
        ..., description="Информация о транспортном средстве", max_length=TableConstantsNames.STANDARD_TEXT_LENGTH_MAX
    )

    trailer_id: int | None = Field(None, description="ID прицепа")
    trailer_info: str | None = Field(
        None, description="Информация о прицепе", max_length=TableConstantsNames.STANDARD_TEXT_LENGTH_MAX
    )

    responsible_id: int | None = Field(None, description="ID ответственного лица")
    responsible_name: str | None = Field(
        None, description="Имя ответственного лица", max_length=TableConstantsNames.STANDARD_LENGTH_STRING
    )
    responsible_iin: str | None = Field(
        None, description="ИИН ответственного лица", max_length=TableConstantsNames.IIN_BIN_LENGTH
    )

    vehicle_tara_kg: int = Field(..., description="Вес транспортного средства в кг")
    measured_at: datetime = Field(..., description="Дата и время взвешивания")

    class Config:
        from_attributes = True


class InitialWeightCDTO(BaseModel):
    history_id: int | None = Field(None, description="ID истории")
    order_id: int | None = Field(None, description="ID заказа")

    zakaz: str | None = Field(None, description="Номер заказа", max_length=TableConstantsNames.SAP_ORDER_LENGTH_STRING)

    vehicle_id: int | None = Field(None, description="ID транспортного средства")
    vehicle_info: str = Field(
        ..., description="Информация о транспортном средстве", max_length=TableConstantsNames.STANDARD_TEXT_LENGTH_MAX
    )

    trailer_id: int | None = Field(None, description="ID прицепа")
    trailer_info: str | None = Field(
        None, description="Информация о прицепе", max_length=TableConstantsNames.STANDARD_TEXT_LENGTH_MAX
    )

    responsible_id: int | None = Field(None, description="ID ответственного лица")
    responsible_name: str | None = Field(
        None, description="Имя ответственного лица", max_length=TableConstantsNames.STANDARD_LENGTH_STRING
    )
    responsible_iin: str | None = Field(
        None, description="ИИН ответственного лица", max_length=TableConstantsNames.IIN_BIN_LENGTH
    )

    vehicle_tara_kg: int = Field(..., description="Вес транспортного средства в кг")
    measured_at: datetime = Field(..., description="Дата и время взвешивания")

    class Config:
        from_attributes = True


class InitialWeightRelationsDTO(InitialWeightRDTO):
    history: ScheduleHistoryRDTO | None = None
    order: OrderRDTO | None = None
    responsible: UserRDTO | None = None
    vehicle: VehicleRDTO | None = None
    trailer: VehicleRDTO | None = None

    class Config:
        from_attributes = True
