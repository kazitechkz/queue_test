from datetime import datetime

from pydantic import BaseModel, Field, condecimal

from app.shared.database_constants import TableConstantsNames


class KaspiPaymentRDTO(BaseModel):
    zakaz: str | None = Field(description="Номер заказа")
    txn_date: str | None = Field(description="Номер заказа")
    sum: condecimal(max_digits=10, decimal_places=2) = Field(
        description="Сумма транзакции с точностью до сотых"
    )
    paid_at: datetime | None = Field(description="Дата оплаты")
    amount: int = Field(description="Количество или объем")

    class Config:
        from_attributes = True


class KaspiPaymentCDTO(BaseModel):
    order_id: int | None = Field(None, description="ID заказа, связанного с оплатой")
    zakaz: str = Field(..., max_length=TableConstantsNames.SAP_ORDER_LENGTH_STRING, description="Номер заказа")
    account: str = Field(..., max_length=TableConstantsNames.SAP_ORDER_LENGTH_STRING, description="Номер счета")
    txn_id: str | None = Field(
        None, max_length=TableConstantsNames.SAP_ORDER_LENGTH_STRING, description="Идентификатор транзакции"
    )
    txn_check_id: str | None = Field(
        None, max_length=TableConstantsNames.SAP_ORDER_LENGTH_STRING, description="Идентификатор проверки транзакции"
    )
    txn_pay_id: str | None = Field(
        None, max_length=TableConstantsNames.SAP_ORDER_LENGTH_STRING, description="Идентификатор оплаты транзакции"
    )
    txn_date: str | None = Field(None, max_length=TableConstantsNames.STANDARD_LENGTH_STRING, description="Дата транзакции")
    command: str | None = Field(None, max_length=TableConstantsNames.SAP_ORDER_LENGTH_STRING, description="Команда транзакции")
    sum: condecimal(max_digits=10, decimal_places=2) = Field(
        ..., description="Сумма транзакции с точностью до сотых"
    )
    amount: int = Field(..., description="Количество или объем")
    is_failed: bool = Field(default=False, description="Неудачная транзакция")
    is_paid: bool = Field(default=False, description="Транзакция оплачена")
    is_qr_generate: bool = Field(default=False, description="QR-код сгенерирован")
    paid_at: datetime | None = Field(None, description="Дата оплаты")

    class Config:
        from_attributes = True  # Allows Pydantic to work with SQLAlchemy ORM objects


class KaspiPaymentCheckResponseDTO(BaseModel):
    txn_id: str = Field(max_length=20, description="Уникальный идентификатор в Kaspi")
    result: int = Field(ge=0, le=TableConstantsNames.SAP_ORDER_LENGTH_STRING, description="Ответ для каспи")
    sum: condecimal(max_digits=10, decimal_places=2) = Field(
        description="Цена с налогами"
    )
    comment: str | None = Field(description="Комментарий")


class KaspiPaymentPayResponseDTO(BaseModel):
    txn_id: str = Field(max_length=TableConstantsNames.SAP_ORDER_LENGTH_STRING, description="Уникальный идентификатор в Kaspi")
    prv_txn_id: str = Field(max_length=TableConstantsNames.SAP_ORDER_LENGTH_STRING, description="Уникальный идентификатор заказа")
    result: int = Field(ge=0, le=5, description="Ответ для каспи")
    sum: condecimal(max_digits=10, decimal_places=2) = Field(
        description="Цена с налогами"
    )
    comment: str | None = Field(description="Комментарий")
