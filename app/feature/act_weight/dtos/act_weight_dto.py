from datetime import datetime

from pydantic import BaseModel, Field, model_validator

from app.feature.order.dtos.order_dto import OrderRDTO
from app.feature.schedule_history.dtos.schedule_history_dto import ScheduleHistoryRDTO
from app.feature.user.dtos.user_dto import UserRDTO
from app.feature.vehicle.dtos.vehicle_dto import VehicleRDTO
from app.shared.database_constants import TableConstantsNames


class ActWeightDTO(BaseModel):
    id: int = Field(..., description="ID акта взвешивания")

    created_at: datetime = Field(..., description="Дата создания записи")
    updated_at: datetime = Field(..., description="Дата обновления записи")

    class Config:
        from_attributes = True


class ActWeightRDTO(ActWeightDTO):
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
        None, description="ИИН ответственного лица", max_length=TableConstantsNames.STANDARD_LENGTH_STRING
    )
    vehicle_tara_kg: int = Field(..., description="Тара транспортного средства (кг)")
    vehicle_netto_kg: int = Field(..., description="Нетто транспортного средства (кг)")
    vehicle_brutto_kg: int = Field(..., description="Брутто транспортного средства (кг)")
    measured_at: datetime = Field(..., description="Дата и время взвешивания")

    class Config:
        from_attributes = True


class ActWeightCDTO(BaseModel):
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
        None, description="ИИН ответственного лица", max_length=TableConstantsNames.STANDARD_LENGTH_STRING
    )
    vehicle_tara_kg: int = Field(..., description="Тара транспортного средства (кг)")
    vehicle_brutto_kg: int = Field(..., description="Брутто транспортного средства (кг)")
    measured_at: datetime = Field(..., description="Дата и время взвешивания")

    class Config:
        from_attributes = True

    @model_validator(mode="after")
    def check_brutto_tara(self):
        vehicle_tara_kg = self.vehicle_tara_kg
        vehicle_brutto_kg = self.vehicle_brutto_kg
        if vehicle_brutto_kg < vehicle_tara_kg:
            msg = "Вес брутто не может быть меньше веса тары"
            raise ValueError(msg)
        return self


class ActWeightRelationsDTO(ActWeightRDTO):
    history: ScheduleHistoryRDTO | None = None
    order: OrderRDTO | None = None
    responsible: UserRDTO | None = None
    vehicle: VehicleRDTO | None = None
    trailer: VehicleRDTO | None = None

    class Config:
        from_attributes = True
