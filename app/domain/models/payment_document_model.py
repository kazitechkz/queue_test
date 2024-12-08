from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.shared.database_constants import ID, AppTableNames, CreatedAt, UpdatedAt


class PaymentDocumentModel(Base):
    __tablename__ = AppTableNames.PaymentDocumentTableName
    id: Mapped[ID]
    file_id: Mapped[int] = mapped_column(
        ForeignKey(
            AppTableNames.FileTableName + ".id", onupdate="cascade", ondelete="restrict"
        ),
        nullable=False,
    )
    order_id: Mapped[int] = mapped_column(
        ForeignKey(
            AppTableNames.OrderTableName + ".id", onupdate="cascade", ondelete="restrict"
        ),
        nullable=False,
    )
    checked_by: Mapped[int | None] = mapped_column(
        ForeignKey(
            AppTableNames.UserTableName + ".id", onupdate="cascade", ondelete="set null"
        ),
        nullable=True,
    )
    status: Mapped[bool | None] = mapped_column(Boolean, nullable=True)
    comment: Mapped[str | None] = mapped_column(Text(), nullable=True)
    checked_at: Mapped[datetime | None] = mapped_column(DateTime(), nullable=True)
    created_at: Mapped[CreatedAt]
    updated_at: Mapped[UpdatedAt]

    file: Mapped["FileModel"] = relationship("FileModel")
    checked: Mapped["UserModel"] = relationship("UserModel", foreign_keys=[checked_by])
    order: Mapped["OrderModel"] = relationship("OrderModel")
