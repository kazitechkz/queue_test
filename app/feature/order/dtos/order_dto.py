from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, Field, condecimal


class CreateIndividualOrderDTO(BaseModel):
    material_sap_id:str = Field(max_length=255,description="Уникальный идентификационный номер материала в SAP")
    quan_t:int = Field(gt=1,description="Кол-во материала в тоннах")

    class Config:
        from_attributes = True


class CreateLegalOrderDTO(BaseModel):
    material_sap_id:str = Field(max_length=255,description="Уникальный идентификационный номер материала в SAP")
    quan_t:int = Field(gt=1,description="Кол-во материала в тоннах")
    dogovor:str = Field(max_length=255,description="Номер договора в SAP")
    organization_id: int = Field(gt=0, description="Организация")

    class Config:
        from_attributes = True

class OrderCDTO(BaseModel):
    status_id: Optional[int] = Field(None, description="ID статуса заказа")
    factory_id: Optional[int] = Field(None, description="ID завода")
    factory_sap_id: str = Field(..., max_length=256, description="SAP ID завода")
    workshop_id: Optional[int] = Field(None, description="ID цеха")
    workshop_sap_id: str = Field(..., max_length=256, description="SAP ID цеха")
    material_id: Optional[int] = Field(None, description="ID материала")
    material_sap_id: str = Field(..., max_length=256, description="SAP ID материала")
    quan_t: int = Field(..., description="Количество материала в тоннах")
    quan: int = Field(..., description="Количество материала")
    quan_released: int = Field(..., description="Количество выпущенного материала")
    quan_booked: int = Field(..., description="Количество забронированного материала")
    quan_left: int = Field(..., description="Оставшееся количество материала")
    executed_cruise: int = Field(0, description="Количество выполненных рейсов")
    price_without_taxes: condecimal(max_digits=10, decimal_places=2) = Field(..., description="Цена без налогов")
    price_with_taxes: condecimal(max_digits=10, decimal_places=2) = Field(..., description="Цена с налогами")
    sap_id: Optional[int] = Field(None, description="ID запроса в SAP")
    zakaz: Optional[str] = Field(None, max_length=20, description="Номер заказа")
    kaspi_id: Optional[int] = Field(None, description="ID платежа Kaspi")
    txn_id: Optional[str] = Field(None, max_length=20, description="Уникальный идентификатор транзакции")
    owner_id: Optional[int] = Field(None, description="ID владельца заказа")
    iin: Optional[str] = Field(None, max_length=12, description="ИИН физического лица")
    name: Optional[str] = Field(None, max_length=255, description="Имя клиента")
    organization_id: Optional[int] = Field(None, description="ID организации")
    bin: Optional[str] = Field(None, max_length=12, description="БИН организации")
    dogovor: Optional[str] = Field(None, max_length=255, description="Номер договора")
    is_active: bool = Field(True, description="Активен ли заказ?")
    is_finished: bool = Field(False, description="Завершен ли заказ?")
    is_failed: bool = Field(False, description="Есть ли ошибки по заказу?")
    is_paid: bool = Field(False, description="Оплачен ли заказ?")
    start_at: datetime = Field(..., description="Дата и время начала заказа")
    end_at: datetime = Field(..., description="Дата завершения заказа")
    finished_at: Optional[datetime] = Field(None, description="Дата фактического завершения заказа")
    paid_at: Optional[datetime] = Field(None, description="Дата оплаты заказа")

    class Config:
        from_attributes = True  # Allows for easy conversion from ORM models



