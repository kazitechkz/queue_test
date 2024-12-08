from datetime import datetime

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
    checked_at: datetime = Field(description="Дата проверки")
    status: int = Field(description="Статус")
    comment: str | None = Field(description="Комментарии к прикрепленному файлу")

    class Config:
        from_attributes = True


class PaymentDocumentCDTO(BaseModel):
    file_id: int | None = Field(..., description="Идентификатор файла")
    order_id: int = Field(..., description="Идентификатор заказа")
    checked_by: int | None = Field(..., description="Ответственный за проверку")
    checked_at: int | None = Field(..., description="Дата проверки")
    status: int | None = Field(..., description="Статус")
    comment: str | None = Field(None, description="Комментарии к прикрепленному файлу")

    class Config:
        from_attributes = True  # Allows Pydantic to work with SQLAlchemy ORM objects


class PaymentDocumentRDTOWithRelations(PaymentDocumentRDTO):
    file: FileRDTO
    checked: UserRDTO | None
    order: OrderRDTO | None

    class Config:
        from_attributes = True
