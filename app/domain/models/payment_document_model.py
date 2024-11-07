from typing import Optional

from sqlalchemy import ForeignKey, Boolean, DateTime, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.shared.database_constants import AppTableNames, ID, CreatedAt, UpdatedAt
from datetime import datetime


class PaymentDocumentModel(Base):
    __tablename__ = AppTableNames.PaymentDocumentTableName
    id: Mapped[ID]
    file_id: Mapped[int] = mapped_column(
        ForeignKey(AppTableNames.FileTableName + ".id", onupdate="cascade", ondelete="restrict"),
        nullable=False)
    order_id: Mapped[int] = mapped_column(
        ForeignKey(AppTableNames.OrderTableName + ".id", onupdate="cascade", ondelete="restrict"),
        nullable=False)
    checked_by: Mapped[Optional[int]] = mapped_column(
        ForeignKey(AppTableNames.UserTableName + ".id", onupdate="cascade", ondelete="set null"),
        nullable=True)
    status: Mapped[Optional[bool]] = mapped_column(Boolean, nullable=True)
    comment: Mapped[Optional[str]] = mapped_column(Text(length=1000), nullable=True)
    checked_at: Mapped[Optional[datetime]] = mapped_column(DateTime(), nullable=True)
    created_at: Mapped[CreatedAt]
    updated_at: Mapped[UpdatedAt]

    file: Mapped["FileModel"] = relationship(
        "FileModel"
    )
    checked: Mapped["UserModel"] = relationship(
        "UserModel", foreign_keys=[checked_by]
    )
    order: Mapped["OrderModel"] = relationship(
        "OrderModel"
    )
