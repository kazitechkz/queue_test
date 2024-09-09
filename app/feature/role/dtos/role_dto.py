import datetime

from pydantic import BaseModel, Field


class RoleDTO(BaseModel):
    id: int


class RoleCDTO(BaseModel):
    title: str = Field(max_length=200)
    value: str = Field(max_length=255)

    class Config:
        from_attributes = True

class RoleUDTO(RoleDTO):
    title: str = Field(max_length=200)
    value: str = Field(max_length=255)

    class Config:
        from_attributes = True

class RoleRDTO(RoleDTO):
    title: str
    value: str
    created_at: datetime.datetime
    updated_at: datetime.datetime

    class Config:
        from_attributes = True