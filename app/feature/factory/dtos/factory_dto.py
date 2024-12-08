from pydantic import BaseModel, Field

from app.shared.database_constants import TableConstantsNames


class FactoryDTO(BaseModel):
    id: int


class FactoryCDTO(BaseModel):
    title: str = Field(max_length=1000, description="Наименование")
    sap_id: str = Field(
        max_length=TableConstantsNames.STANDARD_LENGTH_STRING, description="Уникальный идентификационный номер в SAP"
    )
    status: bool = Field(default=True, description="Действует ли?")

    class Config:
        from_attributes = True


class FactoryRDTO(FactoryDTO):
    title: str
    sap_id: str
    status: bool

    class Config:
        from_attributes = True
