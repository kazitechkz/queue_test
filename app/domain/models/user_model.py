from sqlalchemy import String, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base
from app.shared.database_constants import AppTableNames, ID, CreatedAt, UpdatedAt


class UserModel(Base):
    __tablename__ = AppTableNames.UserTableName
    id: Mapped[ID]
    role_id: Mapped[int] = mapped_column(
        ForeignKey(AppTableNames.RoleTableName + ".id", onupdate="CASCADE", ondelete="CASCADE"))
    type_id: Mapped[int] = mapped_column(
        ForeignKey(AppTableNames.UserTypeTableName + ".id", onupdate="CASCADE", ondelete="CASCADE"))
    name: Mapped[str] = mapped_column(String(255))
    iin: Mapped[str] = mapped_column(String(12), unique=True)
    email: Mapped[str] = mapped_column(String(255), unique=True)
    phone: Mapped[str] = mapped_column(String(255), unique=True)
    password_hash: Mapped[str] = mapped_column(Text())
    status: Mapped[bool] = mapped_column(default=True)
    created_at: Mapped[CreatedAt]
    updated_at: Mapped[UpdatedAt]

    role: Mapped["RoleModel"] = relationship(
        back_populates="users"
    )

    user_type: Mapped["UserTypeModel"] = relationship(
        back_populates="users"
    )

    organizations: Mapped[list["OrganizationModel"]] = relationship(
        back_populates="owner"
    )

    organization_employees:Mapped[list["OrganizationEmployeeModel"]] = relationship(
        back_populates="employee"
    )
