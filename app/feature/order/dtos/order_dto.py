from pydantic import BaseModel, Field


class CreateIndividualOrderDTO(BaseModel):
    material_sap_id:str = Field(max_length=255,description="Уникальный идентификационный номер материала в SAP")
    quan:int = Field(gt=1,description="Кол-во материала в тоннах")


class CreateLegalOrderDTO(BaseModel):
    material_sap_id:str = Field(max_length=255,description="Уникальный идентификационный номер материала в SAP")
    quan:int = Field(gt=1,description="Кол-во материала в тоннах")
    dogovor:str = Field(max_length=255,description="Номер договора в SAP")
    organization_id: int = Field(gt=0, description="Организация")

