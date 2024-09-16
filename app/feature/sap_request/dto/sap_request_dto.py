from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class SapRequestDTO(BaseModel):
    id: int

class SapRequestCDTO(BaseModel):
    order_id: Optional[int] = Field(None, description="Внешний ключ к таблице заказов, может быть пустым")
    werks: Optional[str] = Field(None, max_length=4, description="Код завода в SAP")
    matnr: str = Field(..., max_length=18, description="Код материала в SAP")
    kun_name: Optional[str] = Field(None, max_length=40, description="ФИО физического лица")
    iin: Optional[str] = Field(None, max_length=12, description="ИИН физического лица")
    quan: int = Field(..., description="Объем заказа")
    price: Optional[float] = Field(None, description="Цена")
    dogovor: Optional[str] = Field(None, max_length=10, description="Номер договора")
    status: Optional[str] = Field(..., max_length=1, description="Статус переноса")
    zakaz: Optional[str] = Field(None, max_length=10, description="Номер заказа из SAP")
    text: Optional[str] = Field(None, max_length=50, description="Описание ошибки при переносе")
    pdf: Optional[bytes] = Field(None, description="Счет на предоплату в формате PDF (Base64)")
    date: Optional[datetime.date] = Field(None, description="Дата переноса")
    time: Optional[datetime.time] = Field(None, description="Время переноса")
    is_active: bool = Field(default=True, description="Активен ли запрос?")
    is_failed: bool = Field(default=False, description="Произошел ли сбой при переносе?")
    is_paid: bool = Field(default=False, description="Оплачен ли запрос?")

    class Config:
        from_attributes=True
        arbitrary_types_allowed = True