from pydantic import BaseModel, Field, field_validator, EmailStr

from app.core.validation_rules import TWELVE_DIGITS_REGEX, EMAIL_REGEX, PHONE_REGEX
from app.shared.relation_dtos.user_organization import UserRDTOWithRelations


class AuthRegDTO(BaseModel):
    name: str = Field(description="ФИО пользователя", max_length=255)
    iin: str = Field(description="ИИН пользователя", max_length=255)
    email: str = Field(description="Почта пользователя", max_length=255)
    phone: str = Field(description="Телефон пользователя", max_length=255)
    password: str = Field(description="Пароль пользователя", max_length=255, min_length=4)
    type_id: int = Field(description="Тип пользователя")

    @field_validator('phone')
    def validate_phone(cls, v) -> str:
        if not PHONE_REGEX.match(v):
            raise ValueError('Неверный формат телефона: +7(XXX) XXX-XX-XX')
        return v

    @field_validator('iin')
    def validate_iin(cls, v) -> str:
        if not TWELVE_DIGITS_REGEX.match(v):
            raise ValueError('Неверный формат ИИН')
        return v

    @field_validator('email')
    def validate_email(cls, v) -> EmailStr:
        if not EMAIL_REGEX.match(v):
            raise ValueError('Неверный формат почты')
        return v

    class Config:
        from_attributes = True

class AuthLogDTO(BaseModel):
    email: str = Field(description="Почта пользователя", max_length=255)
    password: str = Field(description="Пароль пользователя", max_length=255, min_length=4)

    @field_validator('email')
    def validate_email(cls, v) -> EmailStr:
        if not EMAIL_REGEX.match(v):
            raise ValueError('Неверный формат почты')
        return v

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str

# Модель токена данных
class TokenData(BaseModel):
    username: UserRDTOWithRelations