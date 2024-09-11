from pydantic import BaseModel, Field


class WorkshopDTO(BaseModel):
    id: int


class WorkshopCDTO(BaseModel):
    title: str = Field(max_length=1000, description="Наименование")
    sap_id: str = Field(max_length=255, description="Уникальный идентификационный номер в SAP")
    status: bool = Field(default=True, description="Действует ли?")
    factory_id: int = Field(description="Уникальный идентфикационный номер завода")
    factory_sap_id: str = Field(description="Уникальный идентфикационный номер завода в SAP")

    class Config:
        from_attributes = True


class WorkshopRDTO(BaseModel):
    title: str
    sap_id: str
    status: bool
    factory_id: int
    factory_sap_id: str

    class Config:
        from_attributes = True


class WorkshopWithRelationsDTO(WorkshopRDTO):
    pass