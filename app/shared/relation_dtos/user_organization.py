from app.feature.organization.dtos.organization_dto import OrganizationRDTO
from app.feature.organization_type.dtos.organization_type_dto import OrganizationTypeRDTO
from app.feature.role.dtos.role_dto import RoleRDTO
from app.feature.user.dtos.user_dto import UserRDTO
from app.feature.user_type.dtos.user_type_dto import UserTypeRDTO


class OrganizationRDTOWithRelations(OrganizationRDTO):
    owner: UserRDTO
    type: OrganizationTypeRDTO

    class Config:
        from_attributes = True


class UserRDTOWithRelations(UserRDTO):
    role: RoleRDTO | None = None
    user_type: UserTypeRDTO | None = None
    organizations: list[OrganizationRDTO] | None = []

    class Config:
        from_attributes = True
