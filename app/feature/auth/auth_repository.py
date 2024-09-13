from datetime import datetime, timedelta
from typing import Optional

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from app.core.base_repository import BaseRepository
from app.core.database import get_db
from app.domain.models.user_model import UserModel

from app.core.app_settings import app_settings

class AuthRepository(BaseRepository[UserModel]):
    def __init__(self, db: Session = Depends(get_db)):
        super().__init__(UserModel, db)
