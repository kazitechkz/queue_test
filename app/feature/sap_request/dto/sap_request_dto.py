from datetime import date as shedule_date
from datetime import time as shedule_time

from pydantic import BaseModel, Field

from app.shared.database_constants import TableConstantsNames


class SapRequestDTO(BaseModel):
    id: int


class SapRequestCDTO(BaseModel):
    order_id: int | None = Field(
        None, description="Внешний ключ к таблице заказов, может быть пустым"
    )
    werks: str | None = Field(None, max_length=TableConstantsNames.WERKS_LENGTH, description="Код завода в SAP")
    matnr: str = Field(..., max_length=TableConstantsNames.MATNR_LENGTH, description="Код материала в SAP")
    kun_name: str | None = Field(None, max_length=40, description="ФИО физического лица")
    iin: str | None = Field(None, max_length=TableConstantsNames.IIN_BIN_LENGTH, description="ИИН физического лица")
    quan: int = Field(..., description="Объем заказа")
    price: float | None = Field(None, description="Цена")
    dogovor: str | None = Field(None, max_length=TableConstantsNames.SAP_ORDER_LENGTH_STRING, description="Номер договора")
    status: str | None = Field(..., max_length=1, description="Статус переноса")
    zakaz: str | None = Field(None, max_length=TableConstantsNames.SAP_ORDER_LENGTH_STRING, description="Номер заказа из SAP")
    text: str | None = Field(
        None, max_length=50, description="Описание ошибки при переносе"
    )
    pdf: bytes | None = Field(
        None, description="Счет на предоплату в формате PDF (Base64)"
    )
    date: shedule_date | None = Field(None, description="Дата переноса")
    time: shedule_time | None = Field(None, description="Время переноса")
    is_active: bool = Field(default=True, description="Активен ли запрос?")
    is_failed: bool = Field(default=False, description="Произошел ли сбой при переносе?")
    is_paid: bool = Field(default=False, description="Оплачен ли запрос?")

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True


class SapRequestRDTO(SapRequestDTO):
    order_id: int | None = Field(
        None, description="Внешний ключ к таблице заказов, может быть пустым"
    )
    werks: str | None = Field(None, max_length=TableConstantsNames.WERKS_LENGTH, description="Код завода в SAP")
    matnr: str = Field(..., max_length=TableConstantsNames.MATNR_LENGTH, description="Код материала в SAP")
    kun_name: str | None = Field(None, max_length=40, description="ФИО физического лица")
    iin: str | None = Field(None, max_length=TableConstantsNames.IIN_BIN_LENGTH, description="ИИН физического лица")
    quan: int = Field(..., description="Объем заказа")
    price: float | None = Field(None, description="Цена")
    dogovor: str | None = Field(None, max_length=TableConstantsNames.SAP_ORDER_LENGTH_STRING, description="Номер договора")
    status: str | None = Field(..., max_length=1, description="Статус переноса")
    zakaz: str | None = Field(None, max_length=TableConstantsNames.SAP_ORDER_LENGTH_STRING, description="Номер заказа из SAP")
    text: str | None = Field(
        None, max_length=50, description="Описание ошибки при переносе"
    )
    pdf: bytes | None = Field(
        None, description="Счет на предоплату в формате PDF (Base64)"
    )
    date: shedule_date | None = Field(None, description="Дата переноса")
    time: shedule_time | None = Field(None, description="Время переноса")
    is_active: bool = Field(default=True, description="Активен ли запрос?")
    is_failed: bool = Field(default=False, description="Произошел ли сбой при переносе?")
    is_paid: bool = Field(default=False, description="Оплачен ли запрос?")

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True
