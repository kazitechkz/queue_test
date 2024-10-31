from datetime import datetime, timedelta
from typing import Optional

from sqlalchemy import ForeignKey, Text, Integer
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base
from app.shared.database_constants import AppTableNames, ID, CreatedAt, UpdatedAt


class BaselineWeightModel(Base):
    __tablename__ = AppTableNames.BaselineWeightTableName
    id: Mapped[ID]
    vehicle_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey(AppTableNames.VehicleTableName + ".id", onupdate="cascade", ondelete="set null"), nullable=True)
    vehicle_info: Mapped[str] = mapped_column(Text(length=1000))
    vehicle_tara_kg: Mapped[int] = mapped_column(Integer())
    measured_at: Mapped[datetime] = mapped_column()
    created_at: Mapped[CreatedAt]
    updated_at: Mapped[UpdatedAt]

    @hybrid_property
    def end_at(self):
        return self.measured_at + timedelta(days=30)
