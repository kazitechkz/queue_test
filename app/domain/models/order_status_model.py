from typing import Optional

from sqlalchemy import Boolean, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.shared.database_constants import AppTableNames, ID, CreatedAt, UpdatedAt


class OrderStatusModel(Base):
    __tablename__ = AppTableNames.OrderStatusTableName
    id: Mapped[ID]
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    value: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    status: Mapped[bool] = mapped_column(Boolean, default=True)
    is_first: Mapped[bool] = mapped_column(Boolean, default=False)
    is_last: Mapped[bool] = mapped_column(Boolean, default=False)
    prev_id: Mapped[Optional[int]] = mapped_column(ForeignKey('order_status.id'), nullable=True)
    next_id: Mapped[Optional[int]] = mapped_column(ForeignKey('order_status.id'), nullable=True)
    created_at: Mapped[CreatedAt]
    updated_at: Mapped[UpdatedAt]

    prev_status: Mapped[Optional["OrderStatusModel"]] = relationship(
                                                                remote_side=[id],
                                                                foreign_keys=[prev_id],
                                                                backref="next_status")

    next_status: Mapped[Optional["OrderStatusModel"]] = relationship(
                                                                remote_side=[id],
                                                                foreign_keys=[next_id],
                                                                backref="prev_status")
