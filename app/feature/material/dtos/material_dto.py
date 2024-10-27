from typing import Optional

from pydantic import BaseModel, Field

from app.feature.workshop.dtos.workshop_dto import WorkshopRDTO


class MaterialDTO(BaseModel):
    id: int


class MaterialCDTO(BaseModel):
    title: str = Field(max_length=1000, description="Наименование")
    sap_id: str = Field(max_length=255, description="Уникальный идентификационный номер в SAP")
    status: bool = Field(default=True, description="Действует ли?")
    price_without_taxes: float = Field(description="Сумма без НДС")
    price_with_taxes: float = Field(description="Сумма с НДС")
    workshop_id: int = Field(description="Уникальный идентфикационный номер цеха")
    workshop_sap_id: str = Field(description="Уникальный идентфикационный номер цеха в SAP")

    class Config:
        from_attributes = True


class MaterialRDTO(MaterialDTO):
    title: str
    sap_id: str
    status: bool
    price_without_taxes: float
    price_with_taxes: float
    workshop_id: int
    workshop_sap_id: str

    class Config:
        from_attributes = True


class MaterialWithRelationsDTO(MaterialRDTO):
    workshop:Optional[WorkshopRDTO] = None

    class Config:
        from_attributes = True
