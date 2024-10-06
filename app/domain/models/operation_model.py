from typing import Optional

from sqlalchemy import String, ForeignKey, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.shared.database_constants import CreatedAt, UpdatedAt, ID, AppTableNames


class OperationModel(Base):
    __tablename__ = AppTableNames.OperationTableName
    id: Mapped[ID]
    title: Mapped[str] = mapped_column(String(length=255))
    value: Mapped[str] = mapped_column(String(length=255), unique=True, index=True)
    role_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey(AppTableNames.RoleTableName + ".id", onupdate="cascade", ondelete="set null"),
        nullable=True)
    role_value: Mapped[str] = mapped_column(String(length=255))
    is_first: Mapped[bool] = mapped_column(Boolean(), default=False)
    is_last: Mapped[bool] = mapped_column(Boolean(), default=False)
    prev_id: Mapped[Optional[int]] = mapped_column(ForeignKey(AppTableNames.OperationTableName + ".id"), nullable=True)
    next_id: Mapped[Optional[int]] = mapped_column(ForeignKey(AppTableNames.OperationTableName + ".id"), nullable=True)
    can_cancel: Mapped[bool] = mapped_column(Boolean())
    created_at: Mapped[CreatedAt]
    updated_at: Mapped[UpdatedAt]

    role:Mapped["RoleModel"] = relationship(
        "RoleModel",
        back_populates="operations",
        foreign_keys=[role_id],
    )

    prev_operation: Mapped[Optional["OperationModel"]] = relationship(
        "OperationModel",
        foreign_keys=[prev_id],
        remote_side="OperationModel.id",
        lazy="select",
    )

    # Отношение к следующему статусу
    next_operation: Mapped[Optional["OperationModel"]] = relationship(
        "OperationModel",
        foreign_keys=[next_id],
        remote_side="OperationModel.id",
        lazy="select",
    )
