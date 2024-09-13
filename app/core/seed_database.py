from sqlalchemy import select, func
from sqlalchemy.orm import Session

from app.shared.database_constants import TableConstantsNames

async def seed_database(db: Session):
    await add_roles(session=db)
    await add_user_types(session=db)
    await add_organization_types(session=db)
    await add_order_status(session=db)
    await add_sap_data(session=db)

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
    from app.domain.models.order_status_model import OrderStatusModel
    count_query = select(func.count()).select_from(OrderStatusModel)
    total_items = await session.scalar(count_query)
    if total_items == 0:
        data = [
            OrderStatusModel(
                id=1,
                title = "Ожидание создания счета предоплаты в SAP",
                value = TableConstantsNames.OrderStatusWaitSap,
                is_first =  True,
                is_last = False,
            ),
            OrderStatusModel(
                id=2,
                title = "Отказ в системе в SAP",
                value = TableConstantsNames.OrderStatusRejectSap,
                is_first =  False,
                is_last = False,
            ),
            OrderStatusModel(
                id=3,
                title="Ожидание оплаты в Kaspi",
                value=TableConstantsNames.OrderStatusWaitPayment,
                is_first=False,
                is_last=False,
            ),
            OrderStatusModel(
                id=4,
                title="Отказ в системе в Kaspi",
                value=TableConstantsNames.OrderStatusRejectPayment,
                is_first=False,
                is_last=False,
            ),
            OrderStatusModel(
                id=5,
                title="Выполняется",
                value=TableConstantsNames.OrderStatusExecuted,
                is_first=False,
                is_last=False,
            ),
            OrderStatusModel(
                id=6,
                title="Завершен",
                value=TableConstantsNames.OrderStatusFinished,
                is_first=False,
                is_last=True,
            ),
        ]
        session.add_all(data)
        await session.commit()
        for item in data:
            order_statuses = await session.execute(select(OrderStatusModel).filter(OrderStatusModel.value == item.value))
            order_status = order_statuses.scalars().first()
            if order_status is not None:
                if item.value == TableConstantsNames.OrderStatusWaitSap:
                    order_status.prev_id = None
                    order_status.next_id = 3
                if item.value == TableConstantsNames.OrderStatusRejectSap:
                    order_status.prev_id = 1
                    order_status.next_id = None
                if item.value == TableConstantsNames.OrderStatusWaitPayment:
                    order_status.prev_id = 1
                    order_status.next_id = 5
                if item.value == TableConstantsNames.OrderStatusRejectPayment:
                    order_status.prev_id = 3
                    order_status.next_id = None
                if item.value == TableConstantsNames.OrderStatusExecuted:
                    order_status.prev_id = 3
                    order_status.next_id = 6
                if item.value == TableConstantsNames.OrderStatusFinished:
                    order_status.prev_id = 5
                    order_status.next_id = None
                await session.commit()

async def add_sap_data(session:Session):
    from app.domain.models.factory_model import FactoryModel
    from app.domain.models.workshop_model import WorkshopModel
    from app.domain.models.material_model import MaterialModel
    #Factory
    count_query = select(func.count()).select_from(FactoryModel)
    total_items = await session.scalar(count_query)
    if total_items == 0:
        data = [
            FactoryModel(
                id = 1,
                title = "Завод 1011",
                sap_id = "1011"
            ),
            FactoryModel(
                id=2,
                title="Завод 1023",
                sap_id="1023"
            ),
        ]

        session.add_all(data)
        await session.commit()
    #Workshop
    count_query = select(func.count()).select_from(WorkshopModel)
    total_items = await session.scalar(count_query)
    if total_items == 0:
        data = [
            WorkshopModel(
                id=1,
                title = "Цех 5404",
                sap_id = "5404",
                factory_id = 1,
                factory_sap_id = "1011"
            ),
            WorkshopModel(
                id=2,
                title="Цех 5407",
                sap_id="5407",
                factory_id=2,
                factory_sap_id="1023"
            )

        ]

        session.add_all(data)
        await session.commit()
    #Material
    count_query = select(func.count()).select_from(MaterialModel)
    total_items = await session.scalar(count_query)
    if total_items == 0:
        data = [
            MaterialModel(
                id=1,
                title= "ПЕСОК ИЗ ШЛАКОВ ВУ ФЕРРОХРОМА 0-5",
                sap_id ="30012553",
                price_without_taxes = 800.00,
                price_with_taxes = 896.00,
                workshop_id = 1,
                workshop_sap_id = "5404"
            ),
            MaterialModel(
                id=2,
                title="ЩЕБЕНЬ ИЗ ШЛАКОВ ВУ ФЕРРОХРОМА 5-20",
                sap_id="80000620",
                price_without_taxes=725.00,
                price_with_taxes=812.00,
                workshop_id=1,
                workshop_sap_id="5404"
            ),
            MaterialModel(
                id=3,
                title="ЩЕБЕНЬ ИЗ ШЛАКОВ ВУ ФЕРРОХРОМА 20-40",
                sap_id="30133840",
                price_without_taxes=275.00,
                price_with_taxes=308.00,
                workshop_id=1,
                workshop_sap_id="5404"
            ),
            MaterialModel(
                id=4,
                title="ПЕСОК ИЗ ШЛАКА ВУ ФХ ОПШ ПЦ№4",
                sap_id="80000860",
                price_without_taxes=800.00,
                price_with_taxes=896.00,
                workshop_id=2,
                workshop_sap_id="5407"
            ),
            MaterialModel(
                id=5,
                title="ЩЕБЕНЬ 5-20 ИЗ ШЛАКА ВУ ФХ ОПШ ПЦ№4",
                sap_id="80000861",
                price_without_taxes=178.57,
                price_with_taxes=200.00,
                workshop_id=2,
                workshop_sap_id="5407"
            ),
            MaterialModel(
                id=6,
                title="ЩЕБЕНЬ 20-40 ИЗ ШЛАКА ВУ ФХ ОПШ ПЦ№4",
                sap_id="80000862",
                price_without_taxes=178.57,
                price_with_taxes=200.00,
                workshop_id=2,
                workshop_sap_id="5407"
            ),
            MaterialModel(
                id=7,
                title="ЩЕБЕНЬ ШЛАКОВЫЙ ДЛЯ ДОР. СТРОИТ 40-70",
                sap_id="80000575",
                price_without_taxes=178.57,
                price_with_taxes=200.00,
                workshop_id=2,
                workshop_sap_id="5407"
            ),
            MaterialModel(
                id=8,
                title="ШЛАК КАМЕНЬ БУТОВЫЙ ВУ ФХ",
                sap_id="30144621",
                price_without_taxes=250.00,
                price_with_taxes=280.00,
                workshop_id=2,
                workshop_sap_id="5407"
            ),
        ]
        session.add_all(data)
        await session.commit()

