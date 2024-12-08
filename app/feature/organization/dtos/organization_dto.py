from pydantic import BaseModel, EmailStr, Field, model_validator

from app.core.validation_rules import TWELVE_DIGITS_REGEX, EMAIL_REGEX, PHONE_REGEX
from app.shared.database_constants import TableConstantsNames


class OrganizationDTO(BaseModel):
    id: int


class OrganizationCDTO(BaseModel):
    full_name: str = Field(max_length=TableConstantsNames.STANDARD_TEXT_LENGTH_MAX, description="Полное наименование компании")
    short_name: str = Field(max_length=TableConstantsNames.STANDARD_TEXT_LENGTH_MAX, description="Короткое наименование компании")
    bin: str = Field(max_length=TableConstantsNames.IIN_BIN_LENGTH, description="Номер БИН")
    bik: str = Field(max_length=9, description="Номер БИК")
    kbe: str = Field(max_length=TableConstantsNames.SAP_ORDER_LENGTH_STRING, description="Номер КБЕ")
    email: EmailStr = Field(max_length=TableConstantsNames.STANDARD_LENGTH_STRING, description="Корпоративная почта")
    phone: str = Field(max_length=TableConstantsNames.STANDARD_LENGTH_STRING, description="Корпоративный телефон")
    address: str = Field(max_length=TableConstantsNames.STANDARD_TEXT_LENGTH_MAX, description="Юридический адрес")
    status: bool = Field(default=True, description="Активен ли")
    owner_id: int = Field(description="Владелец компании", gt=0)
    type_id: int = Field(description="Тип компании", gt=0)

    @model_validator(mode="before")
    def validate_model(cls, values: dict) -> dict:
        # Проверка телефона
        phone = values.get("phone")
        if phone and not PHONE_REGEX.match(phone):
            raise ValueError("Неверный формат телефона: +77XXXXXXXXX")

        # Проверка почты
        email = values.get("email")
        if email and not EMAIL_REGEX.match(email):
            raise ValueError("Неверный формат почты")

        # Проверка БИН
        bin_value = values.get("bin")
        if bin_value and not TWELVE_DIGITS_REGEX.match(bin_value):
            raise ValueError("Неверный формат БИН")

        return values

    class Config:
        from_attributes = True


class OrganizationRDTO(OrganizationDTO):
    full_name: str
    short_name: str
    bin: str
    bik: str
    kbe: str
    email: EmailStr
    phone: str
    address: str
    status: bool
    owner_id: int
    type_id: int

    class Config:
        from_attributes = True
