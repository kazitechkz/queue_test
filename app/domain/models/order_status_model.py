from typing import Optional

from sqlalchemy import Boolean, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.shared.database_constants import ID, AppTableNames, CreatedAt, UpdatedAt, TableConstantsNames


class OrderStatusModel(Base):
    __tablename__ = AppTableNames.OrderStatusTableName
    id: Mapped[ID]
    title: Mapped[str] = mapped_column(String(TableConstantsNames.STANDARD_LENGTH_STRING), nullable=False)
    value: Mapped[str] = mapped_column(String(TableConstantsNames.STANDARD_LENGTH_STRING), unique=True, nullable=False)
    status: Mapped[bool] = mapped_column(Boolean, default=True)
    is_first: Mapped[bool] = mapped_column(Boolean, default=False)
    is_last: Mapped[bool] = mapped_column(Boolean, default=False)
    prev_id: Mapped[int | None] = mapped_column(
        ForeignKey("order_status.id"), nullable=True
    )
    next_id: Mapped[int | None] = mapped_column(
        ForeignKey("order_status.id"), nullable=True
    )
    created_at: Mapped[CreatedAt]
    updated_at: Mapped[UpdatedAt]

    prev_status: Mapped[Optional["OrderStatusModel"]] = relationship(
        "OrderStatusModel",
        foreign_keys=[prev_id],
        remote_side="OrderStatusModel.id",
        lazy="raise",
    )

    # Отношение к следующему статусу
    next_status: Mapped[Optional["OrderStatusModel"]] = relationship(
        "OrderStatusModel",
        foreign_keys=[next_id],
        remote_side="OrderStatusModel.id",
        lazy="raise",
    )
