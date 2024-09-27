from sqlalchemy import Text, String, ForeignKey, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.shared.database_constants import AppTableNames, ID, CreatedAt, UpdatedAt


class OrganizationModel(Base):
    __tablename__ = AppTableNames.OrganizationTableName
    id: Mapped[ID]
    full_name: Mapped[str] = mapped_column(Text())
    short_name: Mapped[str] = mapped_column(Text())
    bin: Mapped[str] = mapped_column(String(length=12), unique=True, index=True)
    bik: Mapped[str] = mapped_column(String(length=9), unique=True, index=True)
    kbe: Mapped[str] = mapped_column(String(length=20), index=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    phone: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    address: Mapped[str] = mapped_column(Text())
    status: Mapped[bool] = mapped_column(default=True)
    owner_id: Mapped[int] = mapped_column(
        ForeignKey(AppTableNames.UserTableName + ".id", ondelete="set null", onupdate="set null"), nullable=True)
    type_id: Mapped[int] = mapped_column(
        ForeignKey(AppTableNames.OrganizationTypeTableName + ".id", ondelete="set null", onupdate="set null"),
        nullable=True)
    created_at: Mapped[CreatedAt]
    updated_at: Mapped[UpdatedAt]

    owner: Mapped["UserModel"] = relationship(
        "UserModel",
        back_populates="organizations"
    )

    type: Mapped["OrganizationTypeModel"] = relationship(
        back_populates="organizations"
    )

    organization_employees: Mapped[list["OrganizationEmployeeModel"]] = relationship(
        back_populates="organization"
    )

    vehicles: Mapped[list["VehicleModel"]] = relationship(
        back_populates="organization"
    )

    orders: Mapped[list["OrderModel"]] = relationship(
        back_populates="organization",
    )