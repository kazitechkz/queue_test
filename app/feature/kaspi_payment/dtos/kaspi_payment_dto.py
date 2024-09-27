from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, Field, condecimal


class KaspiPaymentRDTO(BaseModel):
    zakaz: Optional[str] = Field(description="Номер заказа")
    txn_date: Optional[str] = Field(description="Номер заказа")
    sum: condecimal(max_digits=10, decimal_places=2) = Field(description="Сумма транзакции с точностью до сотых")
    paid_at: Optional[datetime] = Field(description="Дата оплаты")
    amount: int = Field(description="Количество или объем")

    class Config:
        from_attributes = True


class KaspiPaymentCDTO(BaseModel):
    order_id: Optional[int] = Field(None, description="ID заказа, связанного с оплатой")
    zakaz: str = Field(..., max_length=20, description="Номер заказа")
    account: str = Field(..., max_length=20, description="Номер счета")
    txn_id: Optional[str] = Field(None, max_length=20, description="Идентификатор транзакции")
    txn_check_id: Optional[str] = Field(None, max_length=20, description="Идентификатор проверки транзакции")
    txn_pay_id: Optional[str] = Field(None, max_length=20, description="Идентификатор оплаты транзакции")
    txn_date: Optional[str] = Field(None, max_length=256, description="Дата транзакции")
    command: Optional[str] = Field(None, max_length=20, description="Команда транзакции")
    sum: condecimal(max_digits=10, decimal_places=2) = Field(..., description="Сумма транзакции с точностью до сотых")
    amount: int = Field(..., description="Количество или объем")
    is_failed: bool = Field(default=False, description="Неудачная транзакция")
    is_paid: bool = Field(default=False, description="Транзакция оплачена")
    is_qr_generate: bool = Field(default=False, description="QR-код сгенерирован")
    paid_at: Optional[datetime] = Field(None, description="Дата оплаты")

    class Config:
        from_attributes = True  # Allows Pydantic to work with SQLAlchemy ORM objects


class KaspiPaymentCheckResponseDTO(BaseModel):
    txn_id: str = Field(max_length=20, description="Уникальный идентификатор в Kaspi")
    result: int = Field(ge=0, le=5, description="Ответ для каспи")
    sum: condecimal(max_digits=10, decimal_places=2) = Field(description="Цена с налогами")
    comment: Optional[str] = Field(description="Комментарий")


class KaspiPaymentPayResponseDTO(BaseModel):
    txn_id: str = Field(max_length=20, description="Уникальный идентификатор в Kaspi")
    prv_txn_id: str = Field(max_length=20, description="Уникальный идентификатор заказа")
    result: int = Field(ge=0, le=5, description="Ответ для каспи")
    sum: condecimal(max_digits=10, decimal_places=2) = Field(description="Цена с налогами")
    comment: Optional[str] = Field(description="Комментарий")
