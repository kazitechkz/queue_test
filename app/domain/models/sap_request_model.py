from datetime import date, time
from typing import Optional

from sqlalchemy import String, Numeric, Date, Time, LargeBinary, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

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
    status: Mapped[Optional[str]] = mapped_column(String(1), nullable=True)  # Статус переноса
    zakaz: Mapped[Optional[str]] = mapped_column(String(10), index=True, nullable=True)  # № заказа из SAP
    text: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)  # Описание ошибки при переносе
    pdf: Mapped[Optional[bytes]] = mapped_column(LargeBinary,
                                                 nullable=True)  # Счет на предоплату в формате PDF (Base64)
    date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)  # Дата переноса
    time: Mapped[Optional[time]] = mapped_column(Time, nullable=True)
    # Статусы
    is_active: Mapped[bool] = mapped_column(Boolean(), default=True)
    is_failed: Mapped[bool] = mapped_column(Boolean(), default=False)
    is_paid: Mapped[bool] = mapped_column(Boolean(), default=False)
    # Даты
    created_at: Mapped[CreatedAt]
    updated_at: Mapped[UpdatedAt]

    # Связь для "успешного" заказа
    order: Mapped["OrderModel"] = relationship(
        "OrderModel",
        back_populates="sap_request",
        foreign_keys=[order_id],
        overlaps="order_failed"  # Указываем перекрытие с order_failed
    )

    # Связь для "неудачного" заказа
    order_failed: Mapped["OrderModel"] = relationship(
        "OrderModel",
        back_populates="sap_request_failed",
        foreign_keys=[order_id],
        overlaps="order",  # Указываем перекрытие с order
        viewonly=True
    )
