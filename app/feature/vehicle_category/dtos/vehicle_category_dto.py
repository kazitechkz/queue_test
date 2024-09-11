import datetime

from pydantic import Field, BaseModel


class VehicleCategoryDTO(BaseModel):
    id: int


class VehicleCategoryCDTO(BaseModel):
    title: str = Field(max_length=200)
    value: str = Field(max_length=255)

    class Config:
        from_attributes = True


class VehicleCategoryUDTO(VehicleCategoryDTO):
    title: str = Field(max_length=200)
    value: str = Field(max_length=255)

    class Config:
        from_attributes = True


class VehicleCategoryRDTO(VehicleCategoryDTO):
    title: str
    value: str
    created_at: datetime.datetime
    updated_at: datetime.datetime

    class Config:
        from_attributes = True
