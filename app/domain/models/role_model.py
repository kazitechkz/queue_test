from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.shared.database_constants import ID, AppTableNames, CreatedAt, UpdatedAt, TableConstantsNames


class RoleModel(Base):
    __tablename__ = AppTableNames.RoleTableName
    id: Mapped[ID]
    title: Mapped[str] = mapped_column(String(length=TableConstantsNames.STANDARD_LENGTH_STRING))
    value: Mapped[str] = mapped_column(String(length=TableConstantsNames.STANDARD_LENGTH_STRING), unique=True)
    can_auth: Mapped[bool] = mapped_column(default=True)
    created_at: Mapped[CreatedAt]
    updated_at: Mapped[UpdatedAt]

    users: Mapped[list["UserModel"]] = relationship(back_populates="role")

    operations: Mapped[list["OperationModel"]] = relationship(
        "OperationModel", back_populates="role", foreign_keys="[OperationModel.role_id]"
    )
