from datetime import datetime

from pydantic import BaseModel, Field, condecimal

from app.feature.factory.dtos.factory_dto import FactoryRDTO
from app.feature.kaspi_payment.dtos.kaspi_payment_dto import KaspiPaymentRDTO
from app.feature.material.dtos.material_dto import MaterialRDTO
from app.feature.organization.dtos.organization_dto import OrganizationRDTO
from app.feature.sap_request.dto.sap_request_dto import SapRequestRDTO
from app.feature.workshop.dtos.workshop_dto import WorkshopRDTO
from app.shared.database_constants import TableConstantsNames


class OrderRDTO(BaseModel):
    id: int = Field(description="ID заказа")
    status_id: int = Field(description="Статус заказа")

    factory_id: int | None = Field(description="Идентификатор завода")
    factory_sap_id: int = Field(description="Идентификатор завода в системе SAP")

    workshop_id: int | None = Field(description="Идентификатор цеха")
    workshop_sap_id: int = Field(description="Идентификатор цеха в системе SAP")

    material_id: int | None = Field(description="Идентификатор материала")
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

    sap_id: int | None = Field(description="Идентификатор заказа в системе SAP")
    zakaz: str | None = Field(
        description="Сгенерированный счет на предоплату в системе SAP"
    )

    kaspi_id: int | None = Field(description="Идентификатор Каспи")
    txn_id: str | None = Field(description="Сгенерированный номер в системе Каспи")

    owner_id: int | None = Field(description="Идентификатор физ лица")
    iin: str | None = Field(description="ИИН физ лица")
    name: str | None = Field(description="Имя физ лица")

    organization_id: int | None = Field(description="Идентификатор организации")
    bin: str | None = Field(description="БИН/БИК юр лица")
    dogovor: str | None = Field(description="Номер договора")

    is_active: bool = Field(description="Активный заказ")
    is_finished: bool = Field(description="Завершенный заказ")
    is_failed: bool = Field(description="Проваленный заказ")
    is_paid: bool = Field(description="Оплаченный заказ")

    start_at: datetime = Field(description="Начала договора")
    end_at: datetime = Field(description="Конец договора")
    finished_at: datetime | None = Field(description="Время завершения заказа")
    paid_at: datetime | None = Field(description="Время оплаты заказа")

    checked_payment_by_id: int | None = Field(description="Идентификатор бухгалтера")
    checked_payment_by: str | None = Field(description="Имя бухгалтера")
    checked_payment_at: datetime | None = Field(description="Дата проверки")

    must_paid_at: datetime = Field(description="Дата окончания оплаты")
    created_at: datetime = Field(description="Дата создания заказа")
    updated_at: datetime = Field(description="Дата обновления заказа")

    class Config:
        from_attributes = True


class OrderRDTOWithRelations(OrderRDTO):
    material: MaterialRDTO
    organization: OrganizationRDTO | None = None
    factory: FactoryRDTO | None = None
    workshop: WorkshopRDTO | None = None
    kaspi: KaspiPaymentRDTO | None = None
    sap_request: SapRequestRDTO | None = None

    class Config:
        from_attributes = True


class CreateIndividualOrderDTO(BaseModel):
    material_sap_id: str = Field(
        max_length=TableConstantsNames.STANDARD_LENGTH_STRING, description="Уникальный идентификационный номер материала в SAP"
    )
    quan_t: int = Field(ge=1, description="Кол-во материала в тоннах")

    class Config:
        from_attributes = True


class CreateLegalOrderDTO(BaseModel):
    material_sap_id: str = Field(
        max_length=TableConstantsNames.STANDARD_LENGTH_STRING, description="Уникальный идентификационный номер материала в SAP"
    )
    quan_t: int = Field(gt=1, description="Кол-во материала в тоннах")
    dogovor: str = Field(max_length=TableConstantsNames.STANDARD_LENGTH_STRING, description="Номер договора в SAP")
    organization_id: int = Field(gt=0, description="Организация")

    class Config:
        from_attributes = True


class OrderCDTO(BaseModel):
    status_id: int | None = Field(None, description="ID статуса заказа")
    factory_id: int | None = Field(None, description="ID завода")
    factory_sap_id: str = Field(..., max_length=TableConstantsNames.STANDARD_LENGTH_STRING, description="SAP ID завода")
    workshop_id: int | None = Field(None, description="ID цеха")
    workshop_sap_id: str = Field(..., max_length=TableConstantsNames.STANDARD_LENGTH_STRING, description="SAP ID цеха")
    material_id: int | None = Field(None, description="ID материала")
    material_sap_id: str = Field(..., max_length=TableConstantsNames.STANDARD_LENGTH_STRING, description="SAP ID материала")
    quan_t: condecimal(max_digits=10, decimal_places=2) = Field(
        ..., description="Количество материала в тоннах"
    )
    quan: int = Field(..., description="Количество материала")
    quan_released: int = Field(..., description="Количество выпущенного материала")
    quan_released_t: condecimal(max_digits=10, decimal_places=2) = Field(
        None, description="Количество выпущенного материала"
    )
    quan_booked: int = Field(..., description="Количество забронированного материала")
    quan_booked_t: condecimal(max_digits=10, decimal_places=2) = Field(
        None, description="Количество забронированного материала"
    )
    quan_left: int = Field(..., description="Оставшееся количество материала")
    quan_left_t: condecimal(max_digits=10, decimal_places=2) = Field(
        None, description="Оставшееся количество материала"
    )
    executed_cruise: int = Field(0, description="Количество выполненных рейсов")
    price_without_taxes: condecimal(max_digits=10, decimal_places=2) = Field(
        ..., description="Цена без налогов"
    )
    price_with_taxes: condecimal(max_digits=10, decimal_places=2) = Field(
        ..., description="Цена с налогами"
    )
    sap_id: int | None = Field(None, description="ID запроса в SAP")
    zakaz: str | None = Field(None, max_length=TableConstantsNames.SAP_ORDER_LENGTH_STRING, description="Номер заказа")
    kaspi_id: int | None = Field(None, description="ID платежа Kaspi")
    txn_id: str | None = Field(
        None, max_length=20, description="Уникальный идентификатор транзакции"
    )
    owner_id: int | None = Field(None, description="ID владельца заказа")
    iin: str | None = Field(None, max_length=TableConstantsNames.IIN_BIN_LENGTH, description="ИИН физического лица")
    name: str | None = Field(None, max_length=TableConstantsNames.STANDARD_LENGTH_STRING, description="Имя клиента")
    organization_id: int | None = Field(None, description="ID организации")
    bin: str | None = Field(None, max_length=TableConstantsNames.IIN_BIN_LENGTH, description="БИН организации")
    dogovor: str | None = Field(None, max_length=TableConstantsNames.STANDARD_LENGTH_STRING, description="Номер договора")
    is_active: bool = Field(True, description="Активен ли заказ?")
    is_finished: bool = Field(False, description="Завершен ли заказ?")
    is_failed: bool = Field(False, description="Есть ли ошибки по заказу?")
    is_paid: bool = Field(False, description="Оплачен ли заказ?")
    start_at: datetime = Field(..., description="Дата и время начала заказа")
    end_at: datetime = Field(..., description="Дата завершения заказа")
    finished_at: datetime | None = Field(
        None, description="Дата фактического завершения заказа"
    )
    paid_at: datetime | None = Field(None, description="Дата оплаты заказа")

    class Config:
        from_attributes = True  # Allows for easy conversion from ORM models
