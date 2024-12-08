from datetime import datetime

from pydantic import BaseModel, Field

from app.shared.database_constants import TableConstantsNames


class VehicleCategoryDTO(BaseModel):
    id: int


class VehicleCategoryCDTO(BaseModel):
    title: str = Field(max_length=TableConstantsNames.STANDARD_LENGTH_STRING)
    value: str = Field(max_length=TableConstantsNames.STANDARD_LENGTH_STRING)

    class Config:
        from_attributes = True


class VehicleCategoryUDTO(VehicleCategoryDTO):
    title: str = Field(max_length=TableConstantsNames.STANDARD_LENGTH_STRING)
    value: str = Field(max_length=TableConstantsNames.STANDARD_LENGTH_STRING)

    class Config:
        from_attributes = True


class VehicleCategoryRDTO(VehicleCategoryDTO):
    title: str
    value: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
