from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends, Path, Query
from pydantic import EmailStr
from sqlalchemy import and_
from sqlalchemy.orm import selectinload

from app.core.app_exception_response import AppExceptionResponse
from app.core.auth_core import check_client, check_individual_client, check_legal_client
from app.core.pagination_dto import PaginationEmployeeRequestWithRelationDTO
from app.domain.models.employee_request import EmployeeRequestModel
from app.domain.models.organization_employee_model import OrganizationEmployeeModel
from app.feature.employee_request.dtos.employee_request_dto import (
    EmployeeRequestFromEmployeeCDTO,
    EmployeeRequestFromOrganizationCDTO,
    EmployeeRequestRDTO,
    EmployeeRequestWithRelationDTO,
)
from app.feature.employee_request.employee_request_repository import (
    EmployeeRequestRepository,
)
from app.feature.employee_request.filter.employee_request_filter import (
    EmployeeRequestFilter,
)
from app.feature.organization.organization_repository import OrganizationRepository
from app.feature.organization_employee.organization_employee_repository import (
    OrganizationEmployeeRepository,
)
from app.feature.user.dtos.user_dto import UserRDTO
from app.feature.user.user_repository import UserRepository
from app.shared.database_constants import TableConstantsNames
from app.shared.relation_dtos.user_organization import UserRDTOWithRelations


class EmployeeRequestController:
    def __init__(self) -> None:
        self.router = APIRouter()
        self._add_routes()

    def _add_routes(self) -> None:
        # Organization
        self.router.get(
            "/search-employee",
            response_model=Optional[UserRDTO],
            summary="Поиск сотрудника по почте",
            description="Поиск сотрудника по почте в рамках конкретной организации по почте",
        )(self.search_employee)
        self.router.post(
            "/create-request",
            response_model=EmployeeRequestRDTO,
            summary="Создание заявки на включение водителя в компанию",
            description="Создание заявки на включение водителя в компанию в организации",
        )(self.create_request)
        # Both
        self.router.get(
            "/my-requests",
            response_model=PaginationEmployeeRequestWithRelationDTO,
            summary="Мои заявки на включение водителя в компанию",
            description="Мои заявки на включение водителя в компанию в организации",
        )(self.my_requests)
        # Employee
        self.router.put(
            "/make-decision/{id}",
            response_model=EmployeeRequestRDTO,
            summary="Принять или отклонить заявку на включение водителя в компанию",
            description="Принять или отклонить заявку на включение водителя в компанию в организации",
        )(self.make_decision)

    async def search_employee(
        self,
        userDTO: UserRDTOWithRelations = Depends(check_legal_client),
        email: EmailStr = Query(description="Почта сотрудника"),
        organization_id: int = Query(description="Идентификатор организации"),
        userRepo: UserRepository = Depends(UserRepository),
        organizationEmployeeRepo: OrganizationEmployeeRepository = Depends(
            OrganizationEmployeeRepository
        ),
    ):
        organization_employees = await organizationEmployeeRepo.get_all_with_filter(
            filters=[
                and_(organizationEmployeeRepo.model.organization_id == organization_id)
            ]
        )
        employee_ids = [
            organization_employee.employee_id
            for organization_employee in organization_employees
        ]
        finded_user = await userRepo.get_with_filter(
            filters=[
                and_(
                    userRepo.model.email == email,
                    userRepo.model.type_id == TableConstantsNames.UserIndividualTypeId,
                    userRepo.model.id.notin_(employee_ids),
                )
            ]
        )
        return finded_user

    async def my_requests(
        self,
        userDTO: UserRDTOWithRelations = Depends(check_client),
        params: EmployeeRequestFilter = Depends(),
        repo: EmployeeRequestRepository = Depends(EmployeeRequestRepository),
    ):
        filters = params.apply(userDTO=userDTO)
        return await repo.paginate_with_filter(
            dto=EmployeeRequestWithRelationDTO,
            page=params.page,
            per_page=params.per_page,
            filters=filters,
            options=[
                selectinload(repo.model.employee),
                selectinload(repo.model.owner),
                selectinload(repo.model.organization),
            ],
        )

    async def make_decision(
        self,
        userDTO: UserRDTOWithRelations = Depends(check_individual_client),
        id: int = Path(gt=0, description="Идентификатор заявки"),
        dto: EmployeeRequestFromEmployeeCDTO = Depends(),
        repo: EmployeeRequestRepository = Depends(EmployeeRequestRepository),
        organizationEmployeeRepo: OrganizationEmployeeRepository = Depends(
            OrganizationEmployeeRepository
        ),
    ):
        result = await repo.get_with_filter(
            filters=[and_(repo.model.id == id, repo.model.employee_id == userDTO.id)]
        )
        if result is None:
            msg = "Результат не найден"
            raise AppExceptionResponse.bad_request(msg)
        result_dto = EmployeeRequestRDTO.from_orm(result)
        result_dto.status = dto.status
        result_dto.decided_at = datetime.now()
        if dto.status:
            organizationEmployeeModel = OrganizationEmployeeModel(
                organization_id=result.organization_id,
                employee_id=result.employee_id,
            )
            await organizationEmployeeRepo.create(obj=organizationEmployeeModel)
        result_updated = await repo.update(obj=result, dto=result_dto)
        return result_updated

    async def create_request(
        self,
        userDTO: UserRDTOWithRelations = Depends(check_legal_client),
        dto: EmployeeRequestFromOrganizationCDTO = Depends(),
        repo: EmployeeRequestRepository = Depends(EmployeeRequestRepository),
        organizationRepo: OrganizationRepository = Depends(),
        userRepo: UserRepository = Depends(UserRepository),
    ):
        employee_request_old = await repo.get_with_filter(
            filters=[
                and_(
                    repo.model.employee_id == dto.employee_id,
                    repo.model.organization_id == dto.organization_id,
                    repo.model.status is None,
                )
            ]
        )
        if employee_request_old:
            msg = "Вы уже отправили запрос на создание заявки"
            raise AppExceptionResponse.bad_request(msg)
        employee = await userRepo.get_with_filter(
            filters=[
                and_(
                    userRepo.model.id == dto.employee_id,
                    userRepo.model.type_id == TableConstantsNames.UserIndividualTypeId,
                )
            ]
        )
        if employee is None:
            msg = "Работник не найден"
            raise AppExceptionResponse.bad_request(msg)
        organization = await organizationRepo.get(id=dto.organization_id)
        if organization is None:
            msg = "Организация не найдена"
            raise AppExceptionResponse.bad_request(msg)

        employeeRequest = EmployeeRequestModel(
            organization_id=organization.id,
            organization_full_name=organization.full_name,
            organization_bin=organization.bin,
            owner_id=userDTO.id,
            owner_name=userDTO.name,
            employee_id=employee.id,
            employee_name=employee.name,
            employee_email=employee.email,
            status=None,
            requested_at=datetime.now(),
            decided_at=None,
        )
        return await repo.create(obj=employeeRequest)
