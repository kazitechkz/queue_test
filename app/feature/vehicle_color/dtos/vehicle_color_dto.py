from datetime import datetime

from pydantic import BaseModel, Field

from app.shared.database_constants import TableConstantsNames


class VehicleColorDTO(BaseModel):
    id: int


class VehicleColorCDTO(BaseModel):
    title: str = Field(max_length=TableConstantsNames.STANDARD_LENGTH_STRING)
    value: str = Field(max_length=TableConstantsNames.STANDARD_LENGTH_STRING)

    class Config:
        from_attributes = True


class VehicleColorUDTO(VehicleColorDTO):
    title: str = Field(max_length=TableConstantsNames.STANDARD_LENGTH_STRING)
    value: str = Field(max_length=TableConstantsNames.STANDARD_LENGTH_STRING)

    class Config:
        from_attributes = True


class VehicleColorRDTO(VehicleColorDTO):
    title: str
    value: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
