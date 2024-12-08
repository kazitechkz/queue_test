from datetime import datetime

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.shared.database_constants import ID, AppTableNames, CreatedAt, UpdatedAt, TableConstantsNames


class EmployeeRequestModel(Base):
    __tablename__ = AppTableNames.EmployeeRequestTableName

    id: Mapped[ID]

    organization_id: Mapped[int] = mapped_column(
        ForeignKey(
            AppTableNames.OrganizationTableName + ".id",
            ondelete="CASCADE",
            onupdate="CASCADE",
        )
    )
    organization_full_name: Mapped[str] = mapped_column(String(TableConstantsNames.STANDARD_LENGTH_STRING), nullable=True)
    organization_bin: Mapped[str] = mapped_column(String(TableConstantsNames.STANDARD_LENGTH_STRING), nullable=True)

    owner_id: Mapped[int | None] = mapped_column(
        ForeignKey(
            AppTableNames.UserTableName + ".id", onupdate="cascade", ondelete="set null"
        ),
        nullable=True,
    )
    owner_name: Mapped[str] = mapped_column(String(256))

    employee_id: Mapped[int] = mapped_column(
        ForeignKey(
            AppTableNames.UserTableName + ".id", ondelete="CASCADE", onupdate="CASCADE"
        )
    )
    employee_name: Mapped[str] = mapped_column(String(TableConstantsNames.STANDARD_LENGTH_STRING))
    employee_email: Mapped[str] = mapped_column(String(TableConstantsNames.STANDARD_LENGTH_STRING))

    status: Mapped[bool | None] = mapped_column(default=None)  # -1 rejected 1 -approved

    requested_at: Mapped[datetime] = mapped_column()
    decided_at: Mapped[datetime | None] = mapped_column(nullable=True)

    created_at: Mapped[CreatedAt]
    updated_at: Mapped[UpdatedAt]

    organization: Mapped["OrganizationModel"] = relationship(
        "OrganizationModel",
        foreign_keys=[organization_id],
    )

    owner: Mapped["UserModel"] = relationship(
        "UserModel",
        foreign_keys=[owner_id],
    )

    employee: Mapped["UserModel"] = relationship(
        "UserModel",
        foreign_keys=[employee_id],
    )
