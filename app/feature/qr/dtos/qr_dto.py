from pydantic import BaseModel, Field


class QrCDTO(BaseModel):
    order_id: int = Field(description="Номер заказа №")
    zakaz: int = Field(description="Номер заказа в системе SAP")
    start_at: str = Field(description="Начало заезда")
    end_at: str = Field(description="Конец заезда")
    schedule_id: str = Field(description="Номер брони")
