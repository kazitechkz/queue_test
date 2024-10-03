from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, model_validator


class ActWeightDTO(BaseModel):
    id: int = Field(..., description="ID акта взвешивания")

    created_at: datetime = Field(..., description="Дата создания записи")
    updated_at: datetime = Field(..., description="Дата обновления записи")

    class Config:
        from_attributes = True


class ActWeightRDTO(ActWeightDTO):
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

    vehicle_tara_kg: int = Field(..., description="Тара транспортного средства (кг)")
    vehicle_netto_kg: int = Field(..., description="Нетто транспортного средства (кг)")
    vehicle_brutto_kg: int = Field(..., description="Брутто транспортного средства (кг)")

    measured_at: datetime = Field(..., description="Дата и время взвешивания")

    class Config:
        from_attributes = True


class ActWeightCDTO(BaseModel):
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

    vehicle_tara_kg: int = Field(..., description="Тара транспортного средства (кг)")
    vehicle_brutto_kg: int = Field(..., description="Брутто транспортного средства (кг)")

    measured_at: datetime = Field(..., description="Дата и время взвешивания")

    class Config:
        from_attributes = True

    @model_validator(mode='after')
    def check_brutto_tara(self):
        vehicle_tara_kg = self.vehicle_tara_kg
        vehicle_brutto_kg = self.vehicle_brutto_kg
        if vehicle_brutto_kg < vehicle_tara_kg:
            raise ValueError('Вес брутто не может быть меньше веса тары')
        return self