from datetime import datetime

from pydantic import BaseModel, Field

from app.shared.database_constants import TableConstantsNames


class OrganizationTypeDTO(BaseModel):
    id: int


class OrganizationTypeCDTO(BaseModel):
    title: str = Field(max_length=TableConstantsNames.STANDARD_LENGTH_STRING)
    value: str = Field(max_length=TableConstantsNames.STANDARD_LENGTH_STRING)

    class Config:
        from_attributes = True


class OrganizationTypeUDTO(OrganizationTypeDTO):
    title: str = Field(max_length=TableConstantsNames.STANDARD_LENGTH_STRING)
    value: str = Field(max_length=TableConstantsNames.STANDARD_LENGTH_STRING)

    class Config:
        from_attributes = True


class OrganizationTypeRDTO(OrganizationTypeDTO):
    title: str
    value: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
