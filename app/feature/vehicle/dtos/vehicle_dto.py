from datetime import datetime, timezone
from typing import Optional

from pydantic import Field, BaseModel, field_validator, model_validator

from app.feature.organization.dtos.organization_dto import OrganizationRDTO
from app.feature.region.dtos.region_dto import RegionRDTO
from app.feature.user.dtos.user_dto import UserRDTO
from app.feature.vehicle_category.dtos.vehicle_category_dto import VehicleCategoryRDTO
from app.feature.vehicle_color.dtos.vehicle_color_dto import VehicleColorRDTO


class VehicleDTO(BaseModel):
    id: int


class VehicleCDTO(BaseModel):
    document_number: str = Field(max_length=255, description="Номер свидетельства")
    registration_number: str = Field(max_length=255, description="Регистрационный номер")
    car_model: str = Field(max_length=1000, description="Марка Машины")
    start_at: datetime = Field(description="Дата выдачи свидетельства")
    vin: str = Field(description="VIN 17 значный уникальный код")
    produced_at: int = Field(gt=1950, le=datetime.now().year, description="Год выпуска технического средства")
    engine_volume_sm: int = Field(gt=0, description="Объем двигателя в сантиметрах кубических")
    weight_clean_kg: int = Field(gt=0, description="Масса без нагрузки в кг")
    weight_load_max_kg: int = Field(gt=0, description="Масса с максимальной нагрузкой в кг")
    note: Optional[str] = Field(max_length=2000, description="Уникальные отметки")
    deregistration_note: Optional[str] = Field(max_length=2000, description="Отметки о снятии с учета")
    is_trailer: bool = Field(default=False, description="ТС является прицепом")

    category_id: int = Field(gt=0, description="Категория Транспортного Средства")
    color_id: int = Field(gt=0, description="Цвет Транспортного Средства")
    region_id: int = Field(gt=0, description="Место жительства")
    owner_id: Optional[int] = Field(description="Физическое лицо - владелец транспортного средства")
    organization_id: Optional[int] = Field(description="Юридическое лицо - владелец транспортного средства")

    @model_validator(mode="before")
    def check_owner_or_organization(cls, values):
        owner_id = values.get('owner_id')
        organization_id = values.get('organization_id')
        if (owner_id is None and organization_id is None) or (owner_id is not None and organization_id is not None):
            raise ValueError(
                "Вы должны выбрать либо физическое лицо или юридическое лицо,но не оба одновременно."
            )
        return values

    @model_validator(mode="before")
    def check_weight_clean_kg_or_weight_load_max_kg(cls, values):
        weight_clean_kg = values.get('weight_clean_kg')
        weight_load_max_kg = values.get('weight_load_max_kg')
        if weight_load_max_kg < weight_clean_kg:
            raise ValueError(
                "Масса загруженного ТС должен быть больше чем пустой ТС"
            )
        return values

    @field_validator("start_at")
    def validate_start_at(cls, value: datetime):
        min_date = datetime(1900, 1, 1, tzinfo=timezone.utc)  # Приведение к offset-aware
        current_date = datetime.now(timezone.utc)  # Текущая дата также offset-aware

        if not (min_date < value < current_date):
            raise ValueError(f"Дата должна быть больше {min_date} и меньше текущей даты {current_date}.")
        return value

    @field_validator("vin")
    def validate_vin(cls, value):
        if len(value) != 17:
            raise ValueError(f"Вин номер должен быть длиной в 17 знаков.")
        return value

    class Config:
        from_attributes = True


class VehicleRDTO(VehicleDTO):
    document_number: str = Field(max_length=255, description="Номер свидетельства")
    registration_number: str = Field(max_length=255, description="Регистрационный номер")
    car_model: str = Field(max_length=1000, description="Марка Машины")
    start_at: datetime = Field(description="Дата выдачи свидетельства")
    vin: str = Field(description="VIN 17 значный уникальный код")
    produced_at: int = Field(gt=1950, le=datetime.now().year, description="Год выпуска технического средства")
    engine_volume_sm: int = Field(gt=0, description="Объем двигателя в сантиметрах кубических")
    weight_clean_kg: int = Field(gt=0, description="Масса без нагрузки в кг")
    weight_load_max_kg: int = Field(gt=0, description="Масса с максимальной нагрузкой в кг")
    note: Optional[str] = Field(max_length=2000, description="Уникальные отметки")
    deregistration_note: Optional[str] = Field(max_length=2000, description="Отметки о снятии с учета")
    is_trailer: bool = Field(default=False, description="ТС является прицепом")
    category_id: int = Field(gt=0, description="Категория Транспортного Средства")
    color_id: int = Field(gt=0, description="Цвет Транспортного Средства")
    region_id: int = Field(gt=0, description="Место жительства")
    owner_id: Optional[int] = Field(description="Физическое лицо - владелей транспортного средства")
    organization_id: Optional[int] = Field(description="Юридическое лицо - владелей транспортного средства")
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class VehicleWithRelationsDTO(VehicleRDTO):
    category: Optional[VehicleCategoryRDTO]
    color: Optional[VehicleColorRDTO]
    region: Optional[RegionRDTO]
    owner: Optional[UserRDTO]
    organization: Optional[OrganizationRDTO]

    class Config:
        from_attributes = True
