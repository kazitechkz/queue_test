from typing import Optional

from pydantic import BaseModel, Field

from app.feature.file.dtos.file_dto import FileRDTO
from app.feature.order.dtos.order_dto import OrderRDTO
from app.feature.user.dtos.user_dto import UserRDTO


class PaymentDocumentDTO(BaseModel):
    id: int = Field(description="Номер заказа")


class PaymentDocumentRDTO(PaymentDocumentDTO):
    file_id: int = Field(description="Идентификатор файла")
    order_id: int = Field(description="Идентификатор заказа")
    checked_by: int = Field(description="Ответственный за проверку")
    checked_at: int = Field(description="Дата проверки")
    status: int = Field(description="Статус")
    comment: Optional[str] = Field(description="Комментарии к прикрепленному файлу")

    class Config:
        from_attributes = True


class PaymentDocumentCDTO(BaseModel):
    file_id: Optional[int] = Field(..., description="Идентификатор файла")
    order_id: int = Field(..., description="Идентификатор заказа")
    checked_by: Optional[int] = Field(..., description="Ответственный за проверку")
    checked_at: Optional[int] = Field(..., description="Дата проверки")
    status: Optional[int] = Field(..., description="Статус")
    comment: Optional[str] = Field(None, description="Комментарии к прикрепленному файлу")

    class Config:
        from_attributes = True  # Allows Pydantic to work with SQLAlchemy ORM objects


class PaymentDocumentRDTOWithRelations(PaymentDocumentRDTO):
    file: FileRDTO
    checked: Optional[UserRDTO]
    order: Optional[OrderRDTO]

    class Config:
        from_attributes = True
