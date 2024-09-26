from datetime import datetime

from pydantic import Field, BaseModel


class OrganizationTypeDTO(BaseModel):
    id: int


class OrganizationTypeCDTO(BaseModel):
    title: str = Field(max_length=200)
    value: str = Field(max_length=255)

    class Config:
        from_attributes = True


class OrganizationTypeUDTO(OrganizationTypeDTO):
    title: str = Field(max_length=200)
    value: str = Field(max_length=255)

    class Config:
        from_attributes = True


class OrganizationTypeRDTO(OrganizationTypeDTO):
    title: str
    value: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
