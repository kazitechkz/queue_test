from datetime import datetime

from pydantic import BaseModel, Field

from app.shared.database_constants import TableConstantsNames


class BaselineWeightDTO(BaseModel):
    id: int
    created_at: datetime = Field(..., description="Дата и время создания")
    updated_at: datetime = Field(..., description="Дата и время последнего обновления")

    class Config:
        from_attributes = True


class BaselineWeightCDTO(BaseModel):
    vehicle_id: int = Field(None, description="ID транспортного средства")
    vehicle_info: str = Field(
        ..., description="Информация о транспортном средстве", max_length=TableConstantsNames.STANDARD_TEXT_LENGTH_MAX
    )
    vehicle_tara_kg: int = Field(..., description="Вес транспортного средства в кг")
    measured_at: datetime = Field(..., description="Дата и время взвешивания")

    class Config:
        from_attributes = True


class BaselineWeightRDTO(BaseModel):
    vehicle_id: int | None = Field(None, description="ID транспортного средства")
    vehicle_info: str = Field(
        ..., description="Информация о транспортном средстве", max_length=TableConstantsNames.STANDARD_TEXT_LENGTH_MAX
    )
    vehicle_tara_kg: int = Field(..., description="Вес транспортного средства в кг")
    measured_at: datetime = Field(..., description="Дата и время взвешивания")
    end_at: datetime = Field(..., description="Действителен До")

    class Config:
        from_attributes = True
