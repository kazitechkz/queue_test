from typing import Optional, List

from fastapi import APIRouter, Depends, Path
from sqlalchemy import and_
from sqlalchemy.orm import selectinload

from app.core.app_exception_response import AppExceptionResponse
from app.core.auth_core import check_legal_client
from app.domain.models.organization_employee_model import OrganizationEmployeeModel
from app.feature.organization.organization_repository import OrganizationRepository
from app.feature.organization_employee.dtos.organization_employee_dto import OrganizationEmployeeRDTO, \
    OrganizationEmployeeRDTOWithRelations, OrganizationEmployeeCDTO
from app.feature.organization_employee.filter.organization_employee_filter import OrganizationEmployeeFilter
from app.feature.organization_employee.organization_employee_repository import OrganizationEmployeeRepository
from app.feature.user.dtos.user_dto import UserRDTO
from app.feature.user.user_repository import UserRepository
from app.shared.relation_dtos.user_organization import UserRDTOWithRelations


class OrganizationEmployeeController:
    def __init__(self):
        self.router = APIRouter()
        self._add_routes()

    def _add_routes(self):
        self.router.get("/")(self.all)
        self.router.get("/get/{id}", response_model=OrganizationEmployeeRDTOWithRelations)(self.get)
        self.router.get("/my-drivers/{organization_id}",response_model=List[UserRDTO])(self.my_drivers)
        self.router.post("/create", response_model=OrganizationEmployeeRDTO)(self.create)
        self.router.put("/update/{id}", response_model=OrganizationEmployeeRDTO)(self.update)
        self.router.delete("/delete/{id}")(self.delete)

    async def all(self,
                  params: OrganizationEmployeeFilter = Depends(),
                  repo: OrganizationEmployeeRepository = Depends(OrganizationEmployeeRepository)):
        result = await repo.paginate_with_filter(
            dto=OrganizationEmployeeRDTOWithRelations, page=params.page,
            per_page=params.per_page, filters=params.apply(),
            options=[selectinload(OrganizationEmployeeModel.employee), selectinload(OrganizationEmployeeModel.organization)])
        return result
    async def get(self, id: int = Path(gt=0), repo: OrganizationEmployeeRepository = Depends(OrganizationEmployeeRepository)):
        result = await repo.get(id=id,options=[selectinload(OrganizationEmployeeModel.employee), selectinload(OrganizationEmployeeModel.organization)])
        if result is None:
            raise AppExceptionResponse.not_found(message="Организация не найдена")
        return result

    async def my_drivers(
            self,
            organization_id: int = Path(gt=0,description="Уникальный идентификатор организации"),
            userRDTO:UserRDTOWithRelations = Depends(check_legal_client),
            repo: OrganizationEmployeeRepository = Depends(OrganizationEmployeeRepository)
    ):
        users = []
        users.append(UserRDTO.from_orm(userRDTO))
        org_ids = [organization.id for organization in userRDTO.organizations]
        if organization_id not in org_ids:
            raise AppExceptionResponse.bad_request("Вы не имеете доступа к данной организации")

        result = await repo.get_all_with_filter(
            filters=[and_(repo.model.organization_id.in_(org_ids))],
            options=[selectinload(repo.model.employee),
                     selectinload(repo.model.organization)])

        for resultItem in result:
            if resultItem.employee:
                users.append(UserRDTO.from_orm(resultItem.employee))

        return users






    async def create(self,
                     organization_employee_dto: OrganizationEmployeeCDTO,
                     repo: OrganizationEmployeeRepository = Depends(OrganizationEmployeeRepository),
                     userRepo: UserRepository = Depends(UserRepository),
                     organizationRepository=Depends(OrganizationRepository)
                     ):
        await self.check_form(dto=organization_employee_dto, repo=repo, userRepo=userRepo,organizationRepo=organizationRepository)
        result = await repo.create(OrganizationEmployeeModel(**organization_employee_dto.dict()))
        return result

    async def update(self,
                     organization_employee_dto: OrganizationEmployeeCDTO,
                     id: int = Path(gt=0),
                     repo: OrganizationEmployeeRepository = Depends(OrganizationEmployeeRepository),
                     userRepo: UserRepository = Depends(UserRepository),
                     organizationRepository=Depends(OrganizationRepository)
                     ):
        organization_employee = await repo.get(id)
        if organization_employee is None:
            raise AppExceptionResponse.not_found(message="Не найдено")
        await self.check_form(dto=organization_employee_dto,
                              repo=repo,
                              userRepo=userRepo,
                              organizationRepo=organizationRepository, id=id)
        result = await repo.update(obj=organization_employee, dto=organization_employee_dto)
        return result

    async def delete(self, id: int = Path(gt=0), repo: OrganizationEmployeeRepository = Depends(OrganizationEmployeeRepository)):
        await repo.delete(id=id)

    @staticmethod
    async def check_form(
            dto: OrganizationEmployeeCDTO,
            repo: OrganizationEmployeeRepository,
            userRepo: UserRepository,
            organizationRepo: OrganizationRepository,
            id: Optional[int] = None):

        existed_relation = await repo.get_first_with_filters(filters=[
            {"employee_id": dto.employee_id}, {"organization_id": dto.organization_id}
        ])
        if existed_relation is not None:
            if existed_relation.id != id:
                raise AppExceptionResponse.bad_request(message="Работник уже прикреплен к организации")

        employee = await userRepo.get(id=dto.employee_id)
        if employee is None:
            raise AppExceptionResponse.bad_request(message="Работника не существует")

        organization = await organizationRepo.get(id=dto.organization_id)
        if organization is None:
            raise AppExceptionResponse.bad_request(message="Организации не существует")

