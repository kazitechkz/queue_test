from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, Field, condecimal

from app.feature.factory.dtos.factory_dto import FactoryRDTO
from app.feature.kaspi_payment.dtos.kaspi_payment_dto import KaspiPaymentRDTO
from app.feature.material.dtos.material_dto import MaterialRDTO
from app.feature.organization.dtos.organization_dto import OrganizationRDTO
from app.feature.sap_request.dto.sap_request_dto import SapRequestRDTO
from app.feature.workshop.dtos.workshop_dto import WorkshopRDTO


class OrderRDTO(BaseModel):
    id: int = Field(description="ID заказа")
    status_id: int = Field(description="Статус заказа")

    factory_id: Optional[int] = Field(description="Идентификатор завода")
    factory_sap_id: int = Field(description="Идентификатор завода в системе SAP")

    workshop_id: Optional[int] = Field(description="Идентификатор цеха")
    workshop_sap_id: int = Field(description="Идентификатор цеха в системе SAP")

    material_id: Optional[int] = Field(description="Идентификатор материала")
    material_sap_id: int = Field(description="Идентификатор материала в системе SAP")

    quan_t: float = Field(description="Общая масса в т")
    quan: int = Field(description="Общая масса в кг")
    quan_released: int = Field(description="Реализованная масса в кг")
    quan_released_t: float = Field(description="Реализованная масса в т")
    quan_booked: int = Field(description="Забронированная масса в кг")
    quan_booked_t: float = Field(description="Забронированная масса в т")
    quan_left: int = Field(description="Увезенная масса в кг")
    quan_left_t: float = Field(description="Увезенная масса в т")

    executed_cruise: int = Field(description="Количество рейсов")

    price_without_taxes: float = Field(description="Цена без НДС")
    price_with_taxes: float = Field(description="Цена с НДС")

    sap_id: Optional[int] = Field(description="Идентификатор заказа в системе SAP")
    zakaz: Optional[str] = Field(description="Сгенерированный счет на предоплату в системе SAP")

    kaspi_id: Optional[int] = Field(description="Идентификатор Каспи")
    txn_id: Optional[str] = Field(description="Сгенерированный номер в системе Каспи")

    owner_id: Optional[int] = Field(description="Идентификатор физ лица")
    iin: Optional[str] = Field(description="ИИН физ лица")
    name: Optional[str] = Field(description="Имя физ лица")

    organization_id: Optional[int] = Field(description="Идентификатор организации")
    bin: Optional[str] = Field(description="БИН/БИК юр лица")
    dogovor: Optional[str] = Field(description="Номер договора")

    is_active: bool = Field(description="Активный заказ")
    is_finished: bool = Field(description="Завершенный заказ")
    is_failed: bool = Field(description="Проваленный заказ")
    is_paid: bool = Field(description="Оплаченный заказ")

    start_at: datetime = Field(description="Начала договора")
    end_at: datetime = Field(description="Конец договора")
    finished_at: Optional[datetime] = Field(description="Время завершения заказа")
    paid_at: Optional[datetime] = Field(description="Время оплаты заказа")

    checked_payment_by_id: Optional[int] = Field(description="Идентификатор бухгалтера")
    checked_payment_by: Optional[str] = Field(description="Имя бухгалтера")
    checked_payment_at: Optional[datetime] = Field(description="Дата проверки")

    must_paid_at: datetime = Field(description="Дата окончания оплаты")
    created_at: datetime = Field(description="Дата создания заказа")
    updated_at: datetime = Field(description="Дата обновления заказа")

    class Config:
        from_attributes = True


class OrderRDTOWithRelations(OrderRDTO):
    material: MaterialRDTO
    organization: Optional[OrganizationRDTO] = None
    factory: Optional[FactoryRDTO] = None
    workshop: Optional[WorkshopRDTO] = None
    kaspi: Optional[KaspiPaymentRDTO] = None
    sap_request: Optional[SapRequestRDTO] = None

    class Config:
        from_attributes = True


class CreateIndividualOrderDTO(BaseModel):
    material_sap_id: str = Field(max_length=255, description="Уникальный идентификационный номер материала в SAP")
    quan_t: int = Field(ge=1, description="Кол-во материала в тоннах")

    class Config:
        from_attributes = True


class CreateLegalOrderDTO(BaseModel):
    material_sap_id: str = Field(max_length=255, description="Уникальный идентификационный номер материала в SAP")
    quan_t: int = Field(gt=1, description="Кол-во материала в тоннах")
    dogovor: str = Field(max_length=255, description="Номер договора в SAP")
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
    quan_t: condecimal(max_digits=10, decimal_places=2) = Field(..., description="Количество материала в тоннах")
    quan: int = Field(..., description="Количество материала")
    quan_released: int = Field(..., description="Количество выпущенного материала")
    quan_released_t: condecimal(max_digits=10, decimal_places=2) = Field(None,
                                                                         description="Количество выпущенного материала")
    quan_booked: int = Field(..., description="Количество забронированного материала")
    quan_booked_t: condecimal(max_digits=10, decimal_places=2) = Field(None,
                                                                       description="Количество забронированного материала")
    quan_left: int = Field(..., description="Оставшееся количество материала")
    quan_left_t: condecimal(max_digits=10, decimal_places=2) = Field(None,
                                                                     description="Оставшееся количество материала")
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

