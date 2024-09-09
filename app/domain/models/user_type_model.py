from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.shared.database_constants import AppTableNames, CreatedAt, UpdatedAt, ID


class UserTypeModel(Base):
    __tablename__ = AppTableNames.UserTypeTableName
    id: Mapped[ID]
    title: Mapped[str] = mapped_column(String(length=200))
    value: Mapped[str] = mapped_column(String(length=255), unique=True)
    created_at: Mapped[CreatedAt]
    updated_at: Mapped[UpdatedAt]

    users: Mapped[list["UserModel"]] = relationship(
        back_populates="user_type"
    )
