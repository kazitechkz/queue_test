from sqlalchemy import String, Date, Integer, Computed, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.shared.database_constants import AppTableNames, CreatedAt, UpdatedAt, ID
from datetime import datetime


class VehicleModel(Base):
    __tablename__ = AppTableNames.VehicleTableName

    id: Mapped[ID]
    document_number: Mapped[str] = mapped_column(String(length=100), unique=True)
    registration_number: Mapped[str] = mapped_column(String(length=100), unique=True)
    car_model: Mapped[str] = mapped_column(String(length=256))
    start_at: Mapped[datetime] = mapped_column(Date)
    vin: Mapped[str] = mapped_column(String(length=17), unique=True)
    produced_at: Mapped[int] = mapped_column()
    engine_volume_sm: Mapped[int] = mapped_column()
    weight_clean_kg: Mapped[int] = mapped_column()
    weight_load_max_kg: Mapped[int] = mapped_column()
    load_max_kg: Mapped[int] = mapped_column(Computed("weight_load_max_kg - weight_clean_kg"))
    note: Mapped[str] = mapped_column(Text(), nullable=True)
    deregistration_note: Mapped[str] = mapped_column(Text(), nullable=True)
    is_trailer: Mapped[bool] = mapped_column(default=False)

    category_id: Mapped[int] = mapped_column(
        ForeignKey(AppTableNames.VehicleCategoryTableName + ".id", ondelete="set null", onupdate="cascade"),
        nullable=True)
    color_id: Mapped[int] = mapped_column(
        ForeignKey(AppTableNames.VehicleColorTableName + ".id", ondelete="set null", onupdate="cascade"), nullable=True)
    region_id: Mapped[int] = mapped_column(
        ForeignKey(AppTableNames.RegionTableName + ".id", ondelete="set null", onupdate="cascade"), nullable=True)
    owner_id: Mapped[int] = mapped_column(
        ForeignKey(AppTableNames.UserTableName + ".id", ondelete="set null", onupdate="cascade"), nullable=True)
    organization_id: Mapped[int] = mapped_column(
        ForeignKey(AppTableNames.OrganizationTableName + ".id", ondelete="set null", onupdate="cascade"), nullable=True)

    created_at: Mapped[CreatedAt]
    updated_at: Mapped[UpdatedAt]

    category: Mapped["VehicleCategoryModel"] = relationship(
        back_populates="vehicles"
    )

    color: Mapped["VehicleColorModel"] = relationship(
        back_populates="vehicles"
    )

    region: Mapped["RegionModel"] = relationship(
        back_populates="vehicles"
    )

    owner: Mapped["UserModel"] = relationship(
        back_populates="vehicles"
    )

    organization: Mapped["OrganizationModel"] = relationship(
        back_populates="vehicles"
    )

    initial_weights_vehicle:Mapped[list["InitialWeightModel"]] = relationship(
        "InitialWeightModel",
        back_populates="vehicle",
        foreign_keys="[InitialWeightModel.vehicle_id]"
    )
    initial_weights_trailer: Mapped[list["InitialWeightModel"]] = relationship(
        "InitialWeightModel",
        back_populates="trailer",
        foreign_keys="[InitialWeightModel.trailer_id]"
    )