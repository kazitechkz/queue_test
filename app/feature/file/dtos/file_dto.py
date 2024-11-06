from pydantic import BaseModel, Field


class FileDTO(BaseModel):
    id: int


class FileCDTO(BaseModel):
    url: str = Field(max_length=1000, description="URL адрес")
    extension: str = Field(max_length=1000, description="Расширение файла")

    class Config:
        from_attributes = True


class FileRDTO(FileDTO):
    url: str = Field(max_length=1000, description="URL адрес")
    extension: str = Field(max_length=1000, description="Расширение файла")

    class Config:
        from_attributes = True
