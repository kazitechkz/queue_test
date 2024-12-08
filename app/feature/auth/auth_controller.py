from fastapi import APIRouter, Depends

from app.core.app_exception_response import AppExceptionResponse
from app.core.auth_core import (
    create_access_token,
    create_refresh_token,
    get_current_user,
    get_password_hash,
    verify_password,
    verify_refresh_token,
)
from app.domain.models.user_model import UserModel
from app.feature.auth.auth_repository import AuthRepository
from app.feature.auth.dtos.auth_user_dto import AuthLogDTO, AuthRegDTO
from app.feature.role.role_repository import RoleRepository
from app.feature.user.dtos.user_dto import UserRDTO
from app.feature.user.user_repository import UserRepository
from app.feature.user_type.user_type_repository import UserTypeRepository
from app.shared.database_constants import TableConstantsNames
from app.shared.relation_dtos.user_organization import UserRDTOWithRelations


class AuthController:
    def __init__(self) -> None:
        self.router = APIRouter()
        self._add_routes()

    def _add_routes(self) -> None:
        self.router.post("/register", response_model=UserRDTO)(self.register)
        self.router.post("/login")(self.login)
        self.router.post("/refresh")(self.refresh_token)
        self.router.get("/me")(self.me)

    async def register(
        self,
        data: AuthRegDTO,
        repo: UserRepository = Depends(UserRepository),
        authRepo: AuthRepository = Depends(AuthRepository),
        userTypeRepo: UserTypeRepository = Depends(UserTypeRepository),
        roleRepo: RoleRepository = Depends(RoleRepository),
    ):
        existed_by_email = await repo.get_first_with_filters(
            filters=[{"email": data.email}, {"phone": data.phone}, {"iin": data.iin}]
        )
        if existed_by_email is not None:
            if existed_by_email.email == data.email:
                msg = "Пользователь с таким email уже существует"
                raise AppExceptionResponse.bad_request(msg)
            if existed_by_email.phone == data.phone:
                msg = "Пользователь с таким телефоном уже существует"
                raise AppExceptionResponse.bad_request(msg)
            if existed_by_email.iin == data.iin:
                msg = "Пользователь с таким ИИНом уже существует"
                raise AppExceptionResponse.bad_request(msg)
            msg = "Пользователь с такими данными уже существует"
            raise AppExceptionResponse.bad_request(msg)
        existed_type = await userTypeRepo.get(id=data.type_id)
        if existed_type is None:
            msg = "Неверный тип пользователя"
            raise AppExceptionResponse.bad_request(msg)
        existed_role = await roleRepo.get_filtered(
            {"value": TableConstantsNames.RoleClientValue}
        )
        if existed_role is None:
            msg = "Неверный тип пользователя"
            raise AppExceptionResponse.bad_request(msg)
        password = data.password
        dto = data.dict(exclude={"password"})
        dto.update(
            {"password_hash": get_password_hash(password), "role_id": existed_role.id}
        )
        user = UserModel(**dto)
        user = await repo.create(obj=user)
        return user

    async def login(
        self,
        data: AuthLogDTO,
        repo: UserRepository = Depends(UserRepository),
        authRepo: AuthRepository = Depends(AuthRepository),
    ):
        user = await repo.get_filtered(filters={"email": data.email})
        if user is None:
            msg = "Неверный email или пароль"
            raise AppExceptionResponse.bad_request(msg)
        result = verify_password(data.password, user.password_hash)
        if not result:
            msg = "Неверный email или пароль"
            raise AppExceptionResponse.bad_request(msg)
        access_token = create_access_token(data=user.id)
        refresh_token = create_refresh_token(data=user.id)
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
        }

    async def refresh_token(self, token_data: dict = Depends(verify_refresh_token)):
        user_id = token_data.get("sub")
        new_access_token = create_access_token(data=int(user_id))
        return {"access_token": new_access_token, "token_type": "bearer"}

    async def me(self, current_user: UserRDTOWithRelations = Depends(get_current_user)):
        return current_user
