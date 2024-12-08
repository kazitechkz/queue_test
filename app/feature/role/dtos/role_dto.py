from pydantic import BaseModel, Field

from app.shared.database_constants import TableConstantsNames


class RoleDTO(BaseModel):
    id: int


class RoleCDTO(BaseModel):
    title: str = Field(max_length=TableConstantsNames.STANDARD_LENGTH_STRING)
    value: str = Field(max_length=TableConstantsNames.STANDARD_LENGTH_STRING)

    class Config:
        from_attributes = True


class RoleUDTO(RoleDTO):
    title: str = Field(max_length=TableConstantsNames.STANDARD_LENGTH_STRING)
    value: str = Field(max_length=TableConstantsNames.STANDARD_LENGTH_STRING)

    class Config:
        from_attributes = True


class RoleRDTO(RoleDTO):
    title: str
    value: str
    can_auth: bool

    class Config:
        from_attributes = True
