from pydantic import BaseModel, Field, model_validator, EmailStr

from app.core.validation_rules import PHONE_REGEX, TWELVE_DIGITS_REGEX, EMAIL_REGEX
from app.shared.database_constants import TableConstantsNames
from app.shared.relation_dtos.user_organization import UserRDTOWithRelations


class AuthRegDTO(BaseModel):
    name: str = Field(description="ФИО пользователя", max_length=TableConstantsNames.STANDARD_LENGTH_STRING)
    iin: str = Field(description="ИИН пользователя", max_length=TableConstantsNames.STANDARD_LENGTH_STRING)
    email: EmailStr = Field(description="Почта пользователя", max_length=TableConstantsNames.STANDARD_LENGTH_STRING)
    phone: str = Field(description="Телефон пользователя", max_length=TableConstantsNames.STANDARD_LENGTH_STRING)
    password: str = Field(description="Пароль пользователя", max_length=TableConstantsNames.STANDARD_LENGTH_STRING, min_length=TableConstantsNames.MIN_PASSWORD_LENGTH)
    type_id: int = Field(description="Тип пользователя")

    @model_validator(mode="after")
    def validate_model(cls, values: dict) -> dict:
        # Валидация телефона
        phone = values.get("phone")
        if phone and not PHONE_REGEX.match(phone):
            raise ValueError("Неверный формат телефона: +7(XXX) XXX-XX-XX")

        # Валидация ИИН
        iin = values.get("iin")
        if iin and not TWELVE_DIGITS_REGEX.match(iin):
            raise ValueError("Неверный формат ИИН")

        return values

    class Config:
        from_attributes = True


class AuthLogDTO(BaseModel):
    email: EmailStr = Field(description="Почта пользователя", max_length=TableConstantsNames.STANDARD_LENGTH_STRING)
    password: str = Field(description="Пароль пользователя", max_length=TableConstantsNames.STANDARD_LENGTH_STRING, min_length=TableConstantsNames.MIN_PASSWORD_LENGTH)

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str


# Модель токена данных
class TokenData(BaseModel):
    username: UserRDTOWithRelations
