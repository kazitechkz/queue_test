from pydantic import BaseModel, Field


class FactoryDTO(BaseModel):
    id:int

class FactoryCDTO(BaseModel):
    title: str = Field(max_length=1000,description="Наименование")
    sap_id:str = Field(max_length=255,description="никальный идентификационный номер в SAP")
    status: bool = Field(default=True,description="Действует ли?")

    class Config:
        from_attributes = True


class FactoryRDTO(FactoryDTO):
    title: str
    sap_id: str
    status: bool

    class Config:
        from_attributes = True

