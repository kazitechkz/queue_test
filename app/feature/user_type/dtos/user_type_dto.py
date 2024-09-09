import datetime

from pydantic import BaseModel, Field


class UserTypeDTO(BaseModel):
    id: int


class UserTypeCDTO(BaseModel):
    title: str = Field(max_length=200)
    value: str = Field(max_length=255)

    class Config:
        from_attributes = True

class UserTypeUDTO(UserTypeDTO):
    title: str = Field(max_length=200)
    value: str = Field(max_length=255)

    class Config:
        from_attributes = True

class UserTypeRDTO(UserTypeDTO):
    title: str
    value: str
    created_at: datetime.datetime
    updated_at: datetime.datetime

    class Config:
        from_attributes = True