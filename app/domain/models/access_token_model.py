from typing import Optional

from sqlalchemy import ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base
from app.shared.database_constants import AppTableNames, ID, CreatedAt, UpdatedAt


class AccessTokenModel(Base):
    __tablename__ = AppTableNames.AccessTokenTableName
    id: Mapped[ID]
    user_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey(AppTableNames.UserTableName + ".id", onupdate="cascade", ondelete="set null"), nullable=True)
    role_id: Mapped[int] = mapped_column(
        ForeignKey(AppTableNames.RoleTableName + ".id", onupdate="CASCADE", ondelete="CASCADE"))
    token:Mapped[str] = mapped_column(Text())
    created_at: Mapped[CreatedAt]
    updated_at: Mapped[UpdatedAt]