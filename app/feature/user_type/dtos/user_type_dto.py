from pydantic import BaseModel, Field

from app.shared.database_constants import TableConstantsNames


class UserTypeDTO(BaseModel):
    id: int


class UserTypeCDTO(BaseModel):
    title: str = Field(max_length=TableConstantsNames.STANDARD_LENGTH_STRING)
    value: str = Field(max_length=TableConstantsNames.STANDARD_LENGTH_STRING)

    class Config:
        from_attributes = True


class UserTypeUDTO(UserTypeDTO):
    title: str = Field(max_length=TableConstantsNames.STANDARD_LENGTH_STRING)
    value: str = Field(max_length=TableConstantsNames.STANDARD_LENGTH_STRING)

    class Config:
        from_attributes = True


class UserTypeRDTO(UserTypeDTO):
    title: str
    value: str

    class Config:
        from_attributes = True
