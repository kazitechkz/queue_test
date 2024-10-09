from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field

from app.feature.order.dtos.order_dto import OrderRDTO
from app.feature.schedule_history.dtos.schedule_history_dto import ScheduleHistoryRDTO
from app.feature.user.dtos.user_dto import UserRDTO
from app.feature.vehicle.dtos.vehicle_dto import VehicleRDTO


class InitialWeightDTO(BaseModel):
    id: int = Field(..., description="Уникальный идентификатор")

    created_at: datetime = Field(..., description="Дата и время создания")
    updated_at: datetime = Field(..., description="Дата и время последнего обновления")

    class Config:
        from_attributes = True


class InitialWeightRDTO(InitialWeightDTO):
    history_id: Optional[int] = Field(None, description="ID истории")
    order_id: Optional[int] = Field(None, description="ID заказа")

    zakaz: Optional[str] = Field(None, description="Номер заказа", max_length=20)

    vehicle_id: Optional[int] = Field(None, description="ID транспортного средства")
    vehicle_info: str = Field(..., description="Информация о транспортном средстве", max_length=1000)

    trailer_id: Optional[int] = Field(None, description="ID прицепа")
    trailer_info: Optional[str] = Field(None, description="Информация о прицепе", max_length=1000)

    responsible_id: Optional[int] = Field(None, description="ID ответственного лица")
    responsible_name: Optional[str] = Field(None, description="Имя ответственного лица", max_length=256)
    responsible_iin: Optional[str] = Field(None, description="ИИН ответственного лица", max_length=256)

    vehicle_tara_kg: int = Field(..., description="Вес транспортного средства в кг")
    measured_at: datetime = Field(..., description="Дата и время взвешивания")

    class Config:
        from_attributes = True


class InitialWeightCDTO(BaseModel):
    history_id: Optional[int] = Field(None, description="ID истории")
    order_id: Optional[int] = Field(None, description="ID заказа")

    zakaz: Optional[str] = Field(None, description="Номер заказа", max_length=20)

    vehicle_id: Optional[int] = Field(None, description="ID транспортного средства")
    vehicle_info: str = Field(..., description="Информация о транспортном средстве", max_length=1000)

    trailer_id: Optional[int] = Field(None, description="ID прицепа")
    trailer_info: Optional[str] = Field(None, description="Информация о прицепе", max_length=1000)

    responsible_id: Optional[int] = Field(None, description="ID ответственного лица")
    responsible_name: Optional[str] = Field(None, description="Имя ответственного лица", max_length=256)
    responsible_iin: Optional[str] = Field(None, description="ИИН ответственного лица", max_length=256)

    vehicle_tara_kg: int = Field(..., description="Вес транспортного средства в кг")
    measured_at: datetime = Field(..., description="Дата и время взвешивания")

    class Config:
        from_attributes = True
        
        
class InitialWeightRelationsDTO(InitialWeightRDTO):
    history:Optional[ScheduleHistoryRDTO] = None
    order:Optional[OrderRDTO] = None
    responsible:Optional[UserRDTO] = None
    vehicle:Optional[VehicleRDTO] = None
    trailer:Optional[VehicleRDTO] = None

    class Config:
        from_attributes = True
