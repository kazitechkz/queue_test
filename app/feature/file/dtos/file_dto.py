from pydantic import BaseModel, Field

from app.shared.database_constants import TableConstantsNames


class FileDTO(BaseModel):
    id: int


class FileCDTO(BaseModel):
    url: str = Field(max_length=TableConstantsNames.STANDARD_TEXT_LENGTH_MAX, description="URL адрес")
    extension: str = Field(max_length=TableConstantsNames.STANDARD_TEXT_LENGTH_MAX, description="Расширение файла")

    class Config:
        from_attributes = True


class FileRDTO(FileDTO):
    url: str = Field(max_length=TableConstantsNames.STANDARD_TEXT_LENGTH_MAX, description="URL адрес")
    extension: str = Field(max_length=TableConstantsNames.STANDARD_TEXT_LENGTH_MAX, description="Расширение файла")

    class Config:
        from_attributes = True
