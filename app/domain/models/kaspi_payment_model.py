from datetime import datetime

from sqlalchemy import Boolean, ForeignKey, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.shared.database_constants import ID, AppTableNames, CreatedAt, UpdatedAt, TableConstantsNames


class KaspiPaymentModel(Base):
    __tablename__ = AppTableNames.KaspiPaymentsTableName
    id: Mapped[ID]
    order_id: Mapped[int | None] = mapped_column(
        ForeignKey(
            AppTableNames.OrderTableName + ".id", onupdate="cascade", ondelete="set null"
        ),
        nullable=True,
    )
    zakaz: Mapped[str] = mapped_column(String(length=TableConstantsNames.SAP_ORDER_LENGTH_STRING), index=True, nullable=False)
    account: Mapped[str] = mapped_column(String(length=TableConstantsNames.SAP_ORDER_LENGTH_STRING), index=True, nullable=False)
    txn_id: Mapped[str | None] = mapped_column(
        String(length=TableConstantsNames.SAP_ORDER_LENGTH_STRING), index=True, nullable=True
    )
    txn_check_id: Mapped[str | None] = mapped_column(String(length=TableConstantsNames.SAP_ORDER_LENGTH_STRING), nullable=True)
    txn_pay_id: Mapped[str | None] = mapped_column(String(length=TableConstantsNames.SAP_ORDER_LENGTH_STRING), nullable=True)
    txn_date: Mapped[str | None] = mapped_column(String(length=TableConstantsNames.STANDARD_LENGTH_STRING), nullable=True)
    command: Mapped[str | None] = mapped_column(
        String(length=TableConstantsNames.SAP_ORDER_LENGTH_STRING), index=True, nullable=True
    )
    sum: Mapped[float] = mapped_column(Numeric(precision=10, scale=2))
    amount: Mapped[int] = mapped_column()
    is_failed: Mapped[bool] = mapped_column(Boolean(), default=False)
    is_paid: Mapped[bool] = mapped_column(Boolean(), default=False)
    is_qr_generate: Mapped[bool] = mapped_column(Boolean(), default=False)
    paid_at: Mapped[datetime | None] = mapped_column(default=None, nullable=True)
    created_at: Mapped[CreatedAt]
    updated_at: Mapped[UpdatedAt]

    # Связь для "успешного" заказа
    order: Mapped["OrderModel"] = relationship(
        "OrderModel",
        back_populates="kaspi_payment",
        foreign_keys=[order_id],
        overlaps="order_failed",  # Указываем перекрытие с order_failed
    )

    # Связь для "неудачного" заказа
    order_failed: Mapped["OrderModel"] = relationship(
        "OrderModel",
        back_populates="kaspi_payment_failed",
        foreign_keys=[order_id],
        overlaps="order",  # Указываем перекрытие с order
        viewonly=True,
    )
