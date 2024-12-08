from pydantic import BaseModel, Field, model_validator, EmailStr

from app.core.validation_rules import PHONE_REGEX, TWELVE_DIGITS_REGEX, EMAIL_REGEX
from app.shared.database_constants import TableConstantsNames


class UserDTO(BaseModel):
    id: int


class UserCDTO(BaseModel):
    role_id: int = Field(description="Роль пользователя")
    type_id: int = Field(description="Тип пользователя")
    name: str = Field(description="ФИО пользователя", max_length=TableConstantsNames.STANDARD_LENGTH_STRING)
    iin: str
    email: EmailStr
    phone: str
    password_hash: str = Field(
        description="Пароль пользователя", max_length=TableConstantsNames.STANDARD_LENGTH_STRING, min_length=4
    )
    status: bool = Field(description="Статус пользователя", default=True)

    @model_validator(mode="before")
    def validate_fields(cls, values: dict) -> dict:
        # Проверка телефона
        phone = values.get("phone")
        if phone and not PHONE_REGEX.match(phone):
            raise ValueError("Неверный формат телефона: +77XXXXXXXXX")

        # Проверка ИИН
        iin = values.get("iin")
        if iin and not TWELVE_DIGITS_REGEX.match(iin):
            raise ValueError("Неверный формат ИИН")

        return values

    class Config:
        from_attributes = True


class UserRDTO(UserDTO):
    id: int
    role_id: int
    type_id: int
    name: str
    iin: str
    email: EmailStr
    phone: str
    status: bool

    class Config:
        from_attributes = True
