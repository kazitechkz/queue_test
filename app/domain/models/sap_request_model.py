import datetime
from typing import Optional

from sqlalchemy import String, Numeric, Date, Time, LargeBinary, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base
from app.shared.database_constants import AppTableNames, ID, CreatedAt, UpdatedAt


class SapRequestModel(Base):
    __tablename__ = AppTableNames.SAPRequestTableName
    id: Mapped[ID]
    order_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey(AppTableNames.OrderTableName + ".id", onupdate="cascade", ondelete="set null"), nullable=True)
    werks: Mapped[Optional[str]] = mapped_column(String(4), nullable=True)  # Код завода в SAP
    matnr: Mapped[str] = mapped_column(String(18), nullable=False)  # Код материала в SAP
    kun_name: Mapped[str] = mapped_column(String(40), nullable=True)  # ФИО физического лица
    iin: Mapped[Optional[str]] = mapped_column(String(12), nullable=True)  # ИИН физ. лица
    quan: Mapped[int] = mapped_column(Numeric(13, 0), nullable=False)  # Объем заказа
    price: Mapped[Optional[float]] = mapped_column(Numeric(11, 2), nullable=True)  # Цена
    dogovor: Mapped[Optional[str]] = mapped_column(String(10), nullable=True)
    # Поля для результата операции с SAP
    status: Mapped[str] = mapped_column(String(1))  # Статус переноса
    zakaz: Mapped[Optional[str]] = mapped_column(String(10),index=True)  # № заказа из SAP
    text: Mapped[Optional[str]] = mapped_column(String(50))  # Описание ошибки при переносе
    pdf: Mapped[Optional[bytes]] = mapped_column(LargeBinary)  # Счет на предоплату в формате PDF (Base64)
    date: Mapped[Optional[datetime.date]] = mapped_column(Date)  # Дата переноса
    time: Mapped[Optional[datetime.time]] = mapped_column(Time)
    #Статусы
    is_active: Mapped[bool] = mapped_column(Boolean(), default=True)
    is_failed: Mapped[bool] = mapped_column(Boolean(), default=False)
    is_paid: Mapped[bool] = mapped_column(Boolean(), default=False)
    # Даты
    created_at: Mapped[CreatedAt]
    updated_at: Mapped[UpdatedAt]