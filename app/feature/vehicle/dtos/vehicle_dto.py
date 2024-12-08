from datetime import datetime

from dateutil.tz import UTC
from pydantic import BaseModel, Field, model_validator

from app.feature.organization.dtos.organization_dto import OrganizationRDTO
from app.feature.region.dtos.region_dto import RegionRDTO
from app.feature.user.dtos.user_dto import UserRDTO
from app.feature.vehicle_category.dtos.vehicle_category_dto import VehicleCategoryRDTO
from app.feature.vehicle_color.dtos.vehicle_color_dto import VehicleColorRDTO
from app.shared.database_constants import TableConstantsNames


class VehicleDTO(BaseModel):
    id: int


class VehicleCDTO(BaseModel):
    document_number: str = Field(max_length=TableConstantsNames.STANDARD_LENGTH_STRING, description="Номер свидетельства")
    registration_number: str = Field(max_length=TableConstantsNames.STANDARD_LENGTH_STRING, description="Регистрационный номер")
    car_model: str = Field(max_length=TableConstantsNames.STANDARD_TEXT_LENGTH_MAX, description="Марка Машины")
    start_at: datetime = Field(description="Дата выдачи свидетельства")
    vin: str = Field(description="VIN 17 значный уникальный код")
    produced_at: int = Field(
        gt=1950, le=datetime.now().year, description="Год выпуска технического средства"
    )
    engine_volume_sm: int = Field(description="Объем двигателя в сантиметрах кубических")
    weight_clean_kg: int = Field(gt=0, description="Масса без нагрузки в кг")
    weight_load_max_kg: int = Field(
        gt=0, description="Масса с максимальной нагрузкой в кг"
    )
    note: str | None = Field(max_length=TableConstantsNames.LONG_TEXT_LENGTH_MAX, description="Уникальные отметки")
    deregistration_note: str | None = Field(
        max_length=TableConstantsNames.LONG_TEXT_LENGTH_MAX, description="Отметки о снятии с учета"
    )
    is_trailer: bool = Field(default=False, description="ТС является прицепом")

    category_id: int | None = Field(gt=0, description="Категория Транспортного Средства")
    color_id: int | None = Field(gt=0, description="Цвет Транспортного Средства")
    region_id: int | None = Field(gt=0, description="Место жительства")
    owner_id: int | None = Field(
        description="Физическое лицо - владелец транспортного средства"
    )
    organization_id: int | None = Field(
        description="Юридическое лицо - владелец транспортного средства"
    )

    @model_validator(mode="before")
    def check_owner_or_organization(self, values):
        owner_id = values.get("owner_id")
        organization_id = values.get("organization_id")
        if (owner_id is None and organization_id is None) or (
            owner_id is not None and organization_id is not None
        ):
            msg = "Вы должны выбрать либо физическое лицо или юридическое лицо,но не оба одновременно."
            raise ValueError(msg)
        return values

    @model_validator(mode="before")
    def check_weight_clean_kg_or_weight_load_max_kg(self, values):
        weight_clean_kg = values.get("weight_clean_kg")
        weight_load_max_kg = values.get("weight_load_max_kg")
        if weight_load_max_kg < weight_clean_kg:
            msg = "Масса загруженного ТС должен быть больше чем пустой ТС"
            raise ValueError(msg)
        return values

    @model_validator(mode="before")
    def validate_model(cls, values: dict) -> dict:
        # Валидация `start_at`
        start_at = values.get("start_at")
        if start_at:
            if start_at.tzinfo is None:
                start_at = start_at.replace(tzinfo=UTC)  # Приведение к UTC
            min_date = datetime(1900, 1, 1, tzinfo=UTC)
            current_date = datetime.now(UTC)
            if not (min_date < start_at < current_date):
                raise ValueError(
                    f"Дата должна быть больше {min_date} и меньше текущей даты {current_date}."
                )
            values["start_at"] = start_at  # Обновляем значение в словаре

        # Валидация `vin`
        vin = values.get("vin")
        if vin and len(vin) != 17:
            raise ValueError("Вин номер должен быть длиной в 17 знаков.")

        return values

    class Config:
        from_attributes = True


class VehicleRDTO(VehicleDTO):
    document_number: str = Field(max_length=TableConstantsNames.STANDARD_LENGTH_STRING, description="Номер свидетельства")
    registration_number: str = Field(max_length=TableConstantsNames.STANDARD_LENGTH_STRING, description="Регистрационный номер")
    car_model: str = Field(max_length=TableConstantsNames.STANDARD_TEXT_LENGTH_MAX, description="Марка Машины")
    start_at: datetime = Field(description="Дата выдачи свидетельства")
    vin: str = Field(description="VIN 17 значный уникальный код")
    produced_at: int = Field(
        gt=1950, le=datetime.now().year, description="Год выпуска технического средства"
    )
    engine_volume_sm: int = Field(
        gt=0, description="Объем двигателя в сантиметрах кубических"
    )
    weight_clean_kg: int = Field(gt=0, description="Масса без нагрузки в кг")
    weight_load_max_kg: int = Field(
        gt=0, description="Масса с максимальной нагрузкой в кг"
    )
    note: str | None = Field(max_length=TableConstantsNames.LONG_TEXT_LENGTH_MAX, description="Уникальные отметки")
    deregistration_note: str | None = Field(
        max_length=TableConstantsNames.LONG_TEXT_LENGTH_MAX, description="Отметки о снятии с учета"
    )
    is_trailer: bool = Field(default=False, description="ТС является прицепом")
    category_id: int = Field(gt=0, description="Категория Транспортного Средства")
    color_id: int = Field(gt=0, description="Цвет Транспортного Средства")
    region_id: int = Field(gt=0, description="Место жительства")
    owner_id: int | None = Field(
        description="Физическое лицо - владелей транспортного средства"
    )
    organization_id: int | None = Field(
        description="Юридическое лицо - владелей транспортного средства"
    )
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class VehicleWithRelationsDTO(VehicleRDTO):
    category: VehicleCategoryRDTO | None
    color: VehicleColorRDTO | None
    region: RegionRDTO | None
    owner: UserRDTO | None
    organization: OrganizationRDTO | None

    class Config:
        from_attributes = True
