from pydantic import BaseModel, Field, EmailStr, field_validator

from app.core.validation_rules import PHONE_REGEX, EMAIL_REGEX, TWELVE_DIGITS_REGEX
from app.feature.user.dtos.user_dto import UserRDTO


class OrganizationDTO(BaseModel):
    id: int


class OrganizationCDTO(BaseModel):
    full_name: str = Field(max_length=1000, description="Полное наименование компании")
    short_name: str = Field(max_length=1000, description="Короткое наименование компании")
    bin: str = Field(max_length=12, description="Номер БИН")
    bik: str = Field(max_length=9, description="Номер БИК")
    kbe: str = Field(max_length=20, description="Номер КБЕ")
    email: EmailStr = Field(max_length=255, description="Корпоративная почта")
    phone: str = Field(max_length=255, description="Корпоративный телефон")
    address: str = Field(max_length=1000, description="Юридический адрес")
    status: bool = Field(default=True, description="Активен ли")
    owner_id: int = Field(description="Владелец компании", gt=0)
    type_id: bool = Field(description="Тип компании", gt=0)

    @field_validator('phone')
    def validate_phone(cls, v) -> str:
        if not PHONE_REGEX.match(v):
            raise ValueError('Неверный формат телефона: +7(XXX) XXX-XX-XX')
        return v

    @field_validator('email')
    def validate_email(cls, v) -> EmailStr:
        if not EMAIL_REGEX.match(v):
            raise ValueError('Неверный формат почты')
        return v

    @field_validator('bin')
    def validate_bin(cls, v) -> str:
        if not TWELVE_DIGITS_REGEX.match(v):
            raise ValueError('Неверный формат БИН')
        return v

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
    type_id: bool

    class Config:
        from_attributes = True


class OrganizationRDTOWithRelations(OrganizationRDTO):
    owner: UserRDTO
    # Add Type
