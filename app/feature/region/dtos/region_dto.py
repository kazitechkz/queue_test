import datetime

from pydantic import Field, BaseModel


class RegionDTO(BaseModel):
    id: int


class RegionCDTO(BaseModel):
    title: str = Field(max_length=200)
    value: str = Field(max_length=255)

    class Config:
        from_attributes = True

class RegionUDTO(RegionDTO):
    title: str = Field(max_length=200)
    value: str = Field(max_length=255)

    class Config:
        from_attributes = True

class RegionRDTO(RegionDTO):
    title: str
    value: str
    created_at: datetime.datetime
    updated_at: datetime.datetime

    class Config:
        from_attributes = True