from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.shared.database_constants import ID, AppTableNames, CreatedAt, UpdatedAt


class OrganizationEmployeeModel(Base):
    __tablename__ = AppTableNames.OrganizationEmployeeTableName
    id: Mapped[ID]
    organization_id: Mapped[int] = mapped_column(
        ForeignKey(
            AppTableNames.OrganizationTableName + ".id",
            ondelete="CASCADE",
            onupdate="CASCADE",
        )
    )
    employee_id: Mapped[int] = mapped_column(
        ForeignKey(
            AppTableNames.UserTableName + ".id", ondelete="CASCADE", onupdate="CASCADE"
        )
    )
    created_at: Mapped[CreatedAt]
    updated_at: Mapped[UpdatedAt]

    organization: Mapped["OrganizationModel"] = relationship(
        back_populates="organization_employees"
    )

    employee: Mapped["UserModel"] = relationship(back_populates="organization_employees")
