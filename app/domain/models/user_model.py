from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.shared.database_constants import ID, AppTableNames, CreatedAt, UpdatedAt, TableConstantsNames


class UserModel(Base):
    __tablename__ = AppTableNames.UserTableName
    id: Mapped[ID]
    role_id: Mapped[int] = mapped_column(
        ForeignKey(
            AppTableNames.RoleTableName + ".id", onupdate="CASCADE", ondelete="CASCADE"
        )
    )
    type_id: Mapped[int] = mapped_column(
        ForeignKey(
            AppTableNames.UserTypeTableName + ".id",
            onupdate="CASCADE",
            ondelete="CASCADE",
        )
    )
    name: Mapped[str] = mapped_column(String(TableConstantsNames.STANDARD_LENGTH_STRING))
    iin: Mapped[str] = mapped_column(String(12), unique=True)
    email: Mapped[str] = mapped_column(String(TableConstantsNames.STANDARD_LENGTH_STRING), unique=True)
    phone: Mapped[str] = mapped_column(String(TableConstantsNames.STANDARD_LENGTH_STRING), unique=True)
    password_hash: Mapped[str] = mapped_column(Text())
    status: Mapped[bool] = mapped_column(default=True)
    created_at: Mapped[CreatedAt]
    updated_at: Mapped[UpdatedAt]

    role: Mapped["RoleModel"] = relationship(back_populates="users")

    user_type: Mapped["UserTypeModel"] = relationship(back_populates="users")

    organizations: Mapped[list["OrganizationModel"]] = relationship(
        "OrganizationModel", back_populates="owner"
    )

    organization_employees: Mapped[list["OrganizationEmployeeModel"]] = relationship(
        back_populates="employee"
    )

    vehicles: Mapped[list["VehicleModel"]] = relationship(back_populates="owner")

    act_weights: Mapped[list["ActWeightModel"]] = relationship(
        "ActWeightModel",
        back_populates="responsible",
        foreign_keys="[ActWeightModel.responsible_id]",
    )

    initial_weights: Mapped[list["InitialWeightModel"]] = relationship(
        "InitialWeightModel",
        back_populates="responsible",
        foreign_keys="[InitialWeightModel.responsible_id]",
    )

    orders: Mapped[list["OrderModel"]] = relationship(
        "OrderModel", back_populates="owner", foreign_keys="[OrderModel.owner_id]"
    )
