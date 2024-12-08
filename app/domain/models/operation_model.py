from typing import Optional

from sqlalchemy import Boolean, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.shared.database_constants import ID, AppTableNames, CreatedAt, UpdatedAt, TableConstantsNames


class OperationModel(Base):
    __tablename__ = AppTableNames.OperationTableName
    id: Mapped[ID]
    title: Mapped[str] = mapped_column(String(length=TableConstantsNames.STANDARD_LENGTH_STRING))
    value: Mapped[str] = mapped_column(String(length=TableConstantsNames.STANDARD_LENGTH_STRING), unique=True, index=True)
    role_id: Mapped[int | None] = mapped_column(
        ForeignKey(
            AppTableNames.RoleTableName + ".id", onupdate="cascade", ondelete="set null"
        ),
        nullable=True,
    )
    role_value: Mapped[str] = mapped_column(String(length=TableConstantsNames.STANDARD_LENGTH_STRING))
    is_first: Mapped[bool] = mapped_column(Boolean(), default=False)
    is_last: Mapped[bool] = mapped_column(Boolean(), default=False)
    prev_id: Mapped[int | None] = mapped_column(
        ForeignKey(AppTableNames.OperationTableName + ".id"), nullable=True
    )
    next_id: Mapped[int | None] = mapped_column(
        ForeignKey(AppTableNames.OperationTableName + ".id"), nullable=True
    )
    can_cancel: Mapped[bool] = mapped_column(Boolean())
    created_at: Mapped[CreatedAt]
    updated_at: Mapped[UpdatedAt]

    role: Mapped["RoleModel"] = relationship(
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
