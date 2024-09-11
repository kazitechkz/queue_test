import datetime

from pydantic import Field, BaseModel


class VehicleColorDTO(BaseModel):
    id: int


class VehicleColorCDTO(BaseModel):
    title: str = Field(max_length=200)
    value: str = Field(max_length=255)

    class Config:
        from_attributes = True

class VehicleColorUDTO(VehicleColorDTO):
    title: str = Field(max_length=200)
    value: str = Field(max_length=255)

    class Config:
        from_attributes = True

class VehicleColorRDTO(VehicleColorDTO):
    title: str
    value: str
    created_at: datetime.datetime
    updated_at: datetime.datetime

    class Config:
        from_attributes = True