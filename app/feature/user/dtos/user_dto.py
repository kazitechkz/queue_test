from pydantic import BaseModel, Field, EmailStr, field_validator

from app.core.validation_rules import EMAIL_REGEX, TWELVE_DIGITS_REGEX, PHONE_REGEX


class UserDTO(BaseModel):
    id: int


class UserCDTO(BaseModel):
    role_id: int = Field(description="Роль пользователя")
    type_id: int = Field(description="Тип пользователя")
    name: str = Field(description="ФИО пользователя", max_length=255)
    iin: str
    email: str
    phone: str
    password_hash: str = Field(description="Пароль пользователя", max_length=255, min_length=4)
    status: bool = Field(description="Статус пользователя", default=True)

    @field_validator('phone')
    def validate_phone(cls, v) -> str:
        if not PHONE_REGEX.match(v):
            raise ValueError('Неверный формат телефона: +77XXXXXXXXX')
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


class UserRDTO(UserDTO):
    id: int
    role_id: int
    type_id: int
    name: str
    iin: str
    email: str
    phone: str
    status: bool

    class Config:
        from_attributes = True



