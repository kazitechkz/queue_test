from datetime import datetime, timedelta
from typing import Optional

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer,HTTPBearer
from jose import jwt
from passlib.context import CryptContext
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session, selectinload
from starlette import status
import bcrypt
from app.core.app_settings import app_settings
from app.core.database import get_db
from app.domain.models.user_model import UserModel
from app.feature.user.dtos.user_dto import UserRDTOWithRelations
from app.shared.database_constants import TableConstantsNames

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/auth/login')
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


# Функция для создания токена доступа
def create_access_token(data: int):
    to_encode = {}
    to_encode["sub"] = str(data)
    expire = datetime.now() + timedelta(minutes=app_settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire.timestamp()})
    encoded_jwt = jwt.encode(to_encode, app_settings.SECRET_KEY, algorithm=app_settings.ALGORITHM)
    return encoded_jwt

def verify_jwt_token(token:str = Depends(oauth2_scheme)) -> dict:
    try:
        decoded_data = jwt.decode(token, app_settings.SECRET_KEY, algorithms=app_settings.ALGORITHM)
        return decoded_data
    except jwt.JWTError as jwtError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Не удалось проверить токен {str(jwtError)}",
            headers={"WWW-Authenticate": "Bearer"},
        )
async def get_current_user(
    token: str = Depends(verify_jwt_token),
    db: AsyncSession = Depends(get_db)
) -> UserRDTOWithRelations:
    # Проверка истечения срока действия токена
    expire = token.get("exp")
    if not expire or int(expire) < datetime.now().timestamp():
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Срок действия токена истек",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Получение идентификатора пользователя
    user_id = token.get("sub")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Пользователь не найден {str(user_id)}",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Запрос к базе данных для получения пользователя
    query = select(UserModel).options(
        selectinload(UserModel.role),
        selectinload(UserModel.user_type)
    ).filter(UserModel.id == user_id)

    result = await db.execute(query)
    user = result.scalars().first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Пользователь не найден",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Преобразование ORM-модели в DTO
    return UserRDTOWithRelations.from_orm(user)



def check_admin(current_user: UserRDTOWithRelations = Depends(get_current_user)):
    if current_user.role.value != TableConstantsNames.RoleAdminValue:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Отказано в доступе",
        )
    return current_user

def check_security(current_user: UserRDTOWithRelations = Depends(get_current_user)):
    if current_user.role.value != TableConstantsNames.RoleSecurityValue:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Отказано в доступе",
        )
    return current_user

def check_security_loader(current_user: UserRDTOWithRelations = Depends(get_current_user)):
    if current_user.role.value != TableConstantsNames.RoleSecurityLoaderValue:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Отказано в доступе",
        )
    return current_user

def check_loader(current_user: UserRDTOWithRelations = Depends(get_current_user)):
    if current_user.role.value != TableConstantsNames.RoleLoaderValue:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Отказано в доступе",
        )
    return current_user

def check_weigher(current_user: UserRDTOWithRelations = Depends(get_current_user)):
    if current_user.role.value != TableConstantsNames.RoleWeigherValue:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Отказано в доступе",
        )
    return current_user

def check_client(current_user: UserRDTOWithRelations = Depends(get_current_user)):
    if current_user.role.value != TableConstantsNames.RoleClientValue:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Отказано в доступе",
        )
    return current_user

def check_individual_client(current_user: UserRDTOWithRelations = Depends(get_current_user)):
    if current_user.role.value != TableConstantsNames.RoleClientValue:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Отказано в доступе",
        )
    if current_user.user_type.value != TableConstantsNames.UserIndividualTypeValue:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Отказано в доступе",
        )
    return current_user

def check_legal_client(current_user: UserRDTOWithRelations = Depends(get_current_user)):
    if current_user.role.value != TableConstantsNames.RoleClientValue:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Отказано в доступе",
        )
    if current_user.user_type.value != TableConstantsNames.UserLegalTypeValue:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Отказано в доступе",
        )
    return current_user