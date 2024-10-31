from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class BaselineWeightDTO(BaseModel):
    id: int
    created_at: datetime = Field(..., description="Дата и время создания")
    updated_at: datetime = Field(..., description="Дата и время последнего обновления")

    class Config:
        from_attributes = True


class BaselineWeightCDTO(BaseModel):
    vehicle_id: int = Field(None, description="ID транспортного средства")
    vehicle_info: str = Field(..., description="Информация о транспортном средстве", max_length=1000)
    vehicle_tara_kg: int = Field(..., description="Вес транспортного средства в кг")
    measured_at: datetime = Field(..., description="Дата и время взвешивания")

    class Config:
        from_attributes = True


class BaselineWeightRDTO(BaseModel):
    vehicle_id: Optional[int] = Field(None, description="ID транспортного средства")
    vehicle_info: str = Field(..., description="Информация о транспортном средстве", max_length=1000)
    vehicle_tara_kg: int = Field(..., description="Вес транспортного средства в кг")
    measured_at: datetime = Field(..., description="Дата и время взвешивания")
    end_at: datetime = Field(..., description="Действителен До")

    class Config:
        from_attributes = True
