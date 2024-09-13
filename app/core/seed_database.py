from sqlalchemy import select, func
from sqlalchemy.orm import Session

from app.shared.database_constants import TableConstantsNames

async def seed_database(db: Session):
    await add_roles(session=db)
    await add_user_types(session=db)
    await add_organization_types(session=db)

async def add_roles(session:Session):
    from app.domain.models.role_model import RoleModel
    count_query = select(func.count()).select_from(RoleModel)
    total_items = await session.scalar(count_query)
    if total_items == 0:
        data = [
            RoleModel(title="Администратор", value=TableConstantsNames.RoleAdminValue),
            RoleModel(title="Служба Безопасности КПП", value=TableConstantsNames.RoleSecurityValue),
            RoleModel(title="Служба Безопасности Погрузки", value=TableConstantsNames.RoleSecurityLoaderValue),
            RoleModel(title="Погрузчик", value=TableConstantsNames.RoleLoaderValue),
            RoleModel(title="Весовщик", value=TableConstantsNames.RoleWeigherValue),
            RoleModel(title="Клиент", value=TableConstantsNames.RoleClientValue),
        ]

        session.add_all(data)
        await session.commit()


async def add_user_types(session: Session):
    from app.domain.models.user_type_model import UserTypeModel
    count_query = select(func.count()).select_from(UserTypeModel)
    total_items = await session.scalar(count_query)
    if total_items == 0:
        data = [
            UserTypeModel(title="Физическое лицо", value=TableConstantsNames.UserIndividualTypeValue),
            UserTypeModel(title="Юридическое лицо", value=TableConstantsNames.UserLegalTypeValue),
        ]
        session.add_all(data)
        await session.commit()

async def add_organization_types(session: Session):
    from app.domain.models.organization_type_model import OrganizationTypeModel
    count_query = select(func.count()).select_from(OrganizationTypeModel)
    total_items = await session.scalar(count_query)
    if total_items == 0:
        data = [
            OrganizationTypeModel(title="Товарищество с ограниченой ответственностью", value=TableConstantsNames.OrganizationLLCTypeValue),
            OrganizationTypeModel(title="Индивидуальный предприниматель", value=TableConstantsNames.OrganizationIPTypeValue),
        ]
        session.add_all(data)
        await session.commit()

async def add_order_status(session: Session):
    pass