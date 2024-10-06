from datetime import date, time

from sqlalchemy import select, func
from sqlalchemy.orm import Session
from app.shared.database_constants import TableConstantsNames


async def seed_database(db: Session):
    await add_roles(session=db)
    await add_user_types(session=db)
    await add_organization_types(session=db)
    await add_order_status(session=db)
    await add_sap_data(session=db)
    await add_operations(session=db)
    await add_vehicle_colors(session=db)
    await add_vehicle_categories(session=db)
    await add_regions(session=db)
    await add_users(session=db)
    await add_organizations(session=db)
    await add_vehicles(session=db)
    await add_workshop_schedules(session=db)


async def add_roles(session: Session):
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
            OrganizationTypeModel(title="Товарищество с ограниченой ответственностью",
                                  value=TableConstantsNames.OrganizationLLCTypeValue),
            OrganizationTypeModel(title="Индивидуальный предприниматель",
                                  value=TableConstantsNames.OrganizationIPTypeValue),
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
                title="Ожидание создания счета предоплаты в SAP",
                value=TableConstantsNames.OrderStatusWaitSap,
                is_first=True,
                is_last=False,
            ),
            OrderStatusModel(
                id=2,
                title="Отказ в системе в SAP",
                value=TableConstantsNames.OrderStatusRejectSap,
                is_first=False,
                is_last=False,
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
            OrderStatusModel(
                id=7,
                title="Отклонен",
                value=TableConstantsNames.OrderStatusCanceled,
                is_first=False,
                is_last=True,
            ),
        ]
        session.add_all(data)
        await session.commit()
        for item in data:
            order_statuses = await session.execute(
                select(OrderStatusModel).filter(OrderStatusModel.value == item.value))
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


async def add_sap_data(session: Session):
    from app.domain.models.factory_model import FactoryModel
    from app.domain.models.workshop_model import WorkshopModel
    from app.domain.models.material_model import MaterialModel
    # Factory
    count_query = select(func.count()).select_from(FactoryModel)
    total_items = await session.scalar(count_query)
    if total_items == 0:
        data = [
            FactoryModel(
                id=1,
                title="Завод 1011",
                sap_id="1011"
            ),
            FactoryModel(
                id=2,
                title="Завод 1023",
                sap_id="1023"
            ),
        ]

        session.add_all(data)
        await session.commit()
    # Workshop
    count_query = select(func.count()).select_from(WorkshopModel)
    total_items = await session.scalar(count_query)
    if total_items == 0:
        data = [
            WorkshopModel(
                id=1,
                title="Цех 5404",
                sap_id="5404",
                factory_id=1,
                factory_sap_id="1011"
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
    # Material
    count_query = select(func.count()).select_from(MaterialModel)
    total_items = await session.scalar(count_query)
    if total_items == 0:
        data = [
            MaterialModel(
                id=1,
                title="ПЕСОК ИЗ ШЛАКОВ ВУ ФЕРРОХРОМА 0-5",
                sap_id="30012553",
                price_without_taxes=800.00,
                price_with_taxes=896.00,
                workshop_id=1,
                workshop_sap_id="5404"
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


async def add_operations(session: Session):
    from app.domain.models.operation_model import OperationModel
    count_query = select(func.count()).select_from(OperationModel)
    total_items = await session.scalar(count_query)
    if total_items == 0:
        data = [
            OperationModel(
                id=1,
                title="Въезд - Прохождение КПП",
                value=TableConstantsNames.EntryOperationName,
                role_id=TableConstantsNames.RoleSecurityId,
                role_value=TableConstantsNames.RoleSecurityValue,
                can_cancel=True,
                is_first=True,
                is_last=False,
            ),
            OperationModel(
                id=2,
                title="Первичное взвешивание",
                value=TableConstantsNames.InitialWeightOperationName,
                role_id=TableConstantsNames.RoleWeigherId,
                role_value=TableConstantsNames.RoleWeigherValue,
                can_cancel=True,
                is_first=False,
                is_last=False,
            ),
            OperationModel(
                id=3,
                title="Валидация перед погрузкой (СБ)",
                value=TableConstantsNames.LoadingEntryOperationName,
                role_id=TableConstantsNames.RoleSecurityLoaderId,
                role_value=TableConstantsNames.RoleSecurityLoaderValue,
                can_cancel=True,
                is_first=False,
                is_last=False,
            ),
            OperationModel(
                id=4,
                title="Погрузка товара",
                value=TableConstantsNames.LoadingOperationName,
                role_id=TableConstantsNames.RoleLoaderId,
                role_value=TableConstantsNames.RoleLoaderValue,
                can_cancel=True,
                is_first=False,
                is_last=False,
            ),
            OperationModel(
                id=5,
                title="Контрольное взвешивание",
                value=TableConstantsNames.FinalWeightOperationName,
                role_id=TableConstantsNames.RoleWeigherId,
                role_value=TableConstantsNames.RoleWeigherValue,
                can_cancel=True,
                is_first=False,
                is_last=False,
            ),
            OperationModel(
                id=6,
                title="Выезд - Контрольная проверка товара (СБ КПП)",
                value=TableConstantsNames.ExitCheckOperationName,
                role_id=TableConstantsNames.RoleSecurityId,
                role_value=TableConstantsNames.RoleSecurityValue,
                can_cancel=True,
                is_first=False,
                is_last=False,
            ),
            OperationModel(
                id=7,
                title="Служба безопасности:Валидация перед разгрузкой и отменой",
                value=TableConstantsNames.ReLoadingEntryExitOperationName,
                role_id=TableConstantsNames.RoleSecurityLoaderId,
                role_value=TableConstantsNames.RoleSecurityLoaderValue,
                can_cancel=False,
                is_first=False,
                is_last=False,
            ),
            OperationModel(
                id=8,
                title="Разгрузка излишнего товара и выход",
                value=TableConstantsNames.ReLoadingExitOperationName,
                role_id=TableConstantsNames.RoleLoaderId,
                role_value=TableConstantsNames.RoleLoaderValue,
                can_cancel=False,
                is_first=False,
                is_last=True,
            ),
            OperationModel(
                id=9,
                title="Служба безопасности:Валидация перед разгрузкой и взвешиванием",
                value=TableConstantsNames.ReLoadingEntryWeightOperationName,
                role_id=TableConstantsNames.RoleSecurityLoaderId,
                role_value=TableConstantsNames.RoleSecurityLoaderValue,
                can_cancel=False,
                is_first=False,
                is_last=False,
            ),
            OperationModel(
                id=10,
                title="Разгрузка излишнего товара и взвешиванием",
                value=TableConstantsNames.ReLoadingWeightOperationName,
                role_id=TableConstantsNames.RoleLoaderId,
                role_value=TableConstantsNames.RoleLoaderValue,
                can_cancel=False,
                is_first=False,
                is_last=False,
            ),
            OperationModel(
                id=11,
                title="Успешное завершение",
                value=TableConstantsNames.ExecutedOperationName,
                role_id=TableConstantsNames.RoleSecurityId,
                role_value=TableConstantsNames.RoleSecurityValue,
                can_cancel=False,
                is_first=False,
                is_last=True,
            ),
        ]
        session.add_all(data)
        await session.commit()
        for item in data:
            operations = await session.execute(
                select(OperationModel).filter(OperationModel.value == item.value))
            operation = operations.scalars().first()
            if operation is not None:
                if item.value == TableConstantsNames.EntryOperationName:
                    operation.prev_id = None
                    operation.next_id = 2
                if item.value == TableConstantsNames.InitialWeightOperationName:
                    operation.prev_id = 1
                    operation.next_id = 3
                if item.value == TableConstantsNames.LoadingEntryOperationName:
                    operation.prev_id = 2
                    operation.next_id = 4
                if item.value == TableConstantsNames.LoadingOperationName:
                    operation.prev_id = 3
                    operation.next_id = 5
                if item.value == TableConstantsNames.FinalWeightOperationName:
                    operation.prev_id = 4
                    operation.next_id = 6
                if item.value == TableConstantsNames.ExitCheckOperationName:
                    operation.prev_id = 5
                    operation.next_id = 11
                if item.value == TableConstantsNames.ReLoadingEntryExitOperationName:
                    operation.prev_id = 5
                    operation.next_id = 8
                if item.value == TableConstantsNames.ReLoadingExitOperationName:
                    operation.prev_id = 7
                    operation.next_id = None
                if item.value == TableConstantsNames.ReLoadingEntryWeightOperationName:
                    operation.prev_id = 5
                    operation.next_id = 10
                if item.value == TableConstantsNames.ReLoadingWeightOperationName:
                    operation.prev_id = 9
                    operation.next_id = 5
                if item.value == TableConstantsNames.ExecutedOperationName:
                    operation.prev_id = 6
                    operation.next_id = None
                await session.commit()


async def add_vehicle_colors(session: Session):
    from app.domain.models.vehicle_color_model import VehicleColorModel
    count_query = select(func.count()).select_from(VehicleColorModel)
    total_items = await session.scalar(count_query)
    if total_items == 0:
        colors = [
            {"title": "Красный", "value": "red"},
            {"title": "Оранжевый", "value": "orange"},
            {"title": "Жёлтый", "value": "yellow"},
            {"title": "Зелёный", "value": "green"},
            {"title": "Голубой", "value": "light_blue"},
            {"title": "Синий", "value": "blue"},
            {"title": "Фиолетовый", "value": "purple"},
            {"title": "Белый", "value": "white"},
            {"title": "Чёрный", "value": "black"},
            {"title": "Серый", "value": "gray"},
            {"title": "Серебристый", "value": "silver"},
            {"title": "Золотистый", "value": "gold"},
            {"title": "Комбинированный", "value": "combined"}
        ]
        for color in colors:
            # Проверяем, существует ли уже цвет с таким значением
            result = await session.execute(select(VehicleColorModel).filter_by(value=color["value"]))
            existing_color = result.scalars().first()

            if not existing_color:
                # Если цвета нет в базе, добавляем его
                new_color = VehicleColorModel(title=color["title"], value=color["value"])
                session.add(new_color)

            # Сохраняем изменения в базе данных
        await session.commit()


async def add_vehicle_categories(session: Session):
    from app.domain.models.vehicle_category_model import VehicleCategoryModel
    count_query = select(func.count()).select_from(VehicleCategoryModel)
    total_items = await session.scalar(count_query)
    if total_items == 0:
        categories = [
            {"title": "C", "value": "c"},
            {"title": "CE", "value": "ce"},
            {"title": "C1", "value": "c1"},
            {"title": "C1E", "value": "c1e"},

        ]
        for category in categories:
            # Проверяем, существует ли уже цвет с таким значением
            result = await session.execute(select(VehicleCategoryModel).filter_by(value=category["value"]))
            existing_category = result.scalars().first()

            if not existing_category:
                # Если цвета нет в базе, добавляем его
                new_category = VehicleCategoryModel(title=category["title"], value=category["value"])
                session.add(new_category)

            # Сохраняем изменения в базе данных
        await session.commit()


async def add_regions(session: Session):
    from app.domain.models.region_model import RegionModel
    count_query = select(func.count()).select_from(RegionModel)
    total_items = await session.scalar(count_query)
    if total_items == 0:
        regions = [
            {"title": "город Нур-Султан (Астана)", "value": "01"},
            {"title": "город Алма-Ата", "value": "02"},
            {"title": "Акмолинская область", "value": "03"},
            {"title": "Актюбинская область", "value": "04"},
            {"title": "Алма-Атинская область", "value": "05"},
            {"title": "Атырауская область", "value": "06"},
            {"title": "Западно-Казахстанская область", "value": "07"},
            {"title": "Жамбылская область", "value": "08"},
            {"title": "Карагандинская область", "value": "09"},
            {"title": "Костанайская область", "value": "10"},
            {"title": "Кызылординская область", "value": "11"},
            {"title": "Мангистауская область", "value": "12"},
            {"title": "Туркестанская область", "value": "13"},
            {"title": "Павлодарская область", "value": "14"},
            {"title": "Северо-Казахстанская область", "value": "15"},
            {"title": "Восточно-Казахстанская область", "value": "16"},
            {"title": "город Шымкент", "value": "17"}
        ]
        for region in regions:
            result = await session.execute(select(RegionModel).filter_by(value=region["value"]))
            existing_region = result.scalars().first()
            if not existing_region:
                new_region = RegionModel(title=region["title"], value=region["value"])
                session.add(new_region)
                await session.commit()


async def add_users(session: Session):
    from app.domain.models.user_model import UserModel
    from app.core.auth_core import get_password_hash
    count_query = select(func.count()).select_from(UserModel)
    total_items = await session.scalar(count_query)
    if total_items == 0:
        data = [
            UserModel(
                id=1,
                role_id=6,
                type_id=1,
                name="Ширинов Абай",
                iin="970327300931",
                email="mistier.famous@gmail.com",
                phone="+77064205962",
                password_hash=get_password_hash("admin123"),
                status=True
            ),
            UserModel(
                id=2,
                role_id=6,
                type_id=2,
                name="Ширинов Абай Калдыбекович",
                iin="970327300930",
                email="kazitech2023@gmail.com",
                phone="+77064205961",
                password_hash=get_password_hash("admin123"),
                status=True
            ),
            UserModel(
                id=3,
                role_id=6,
                type_id=2,
                name="Мухамедиев Дастан Бахытбекович",
                iin="931011256985",
                email="iutest@gmail.com",
                phone="+77064205963",
                password_hash=get_password_hash("admin123"),
                status=True
            ),
            UserModel(
                id=4,
                role_id=6,
                type_id=1,
                name="Акилбеков Нурбакыт Ниязбекович",
                iin="961011256524",
                email="nurbakit@gmail.com",
                phone="+77064171796",
                password_hash=get_password_hash("admin123"),
                status=True
            ),
            UserModel(
                id=5,
                role_id=2,
                type_id=1,
                name="Охраник Охранников",
                iin="222222222222",
                email="security@gmail.com",
                phone="+77062222222",
                password_hash=get_password_hash("admin123"),
                status=True
            ),
            UserModel(
                id=6,
                role_id=3,
                type_id=1,
                name="Охраник Погрузчиков",
                iin="333333333333",
                email="security_loader@gmail.com",
                phone="+77063333333",
                password_hash=get_password_hash("admin123"),
                status=True
            ),
            UserModel(
                id=7,
                role_id=4,
                type_id=1,
                name="Погрузчик Погрузчиков",
                iin="444444444444",
                email="loader@gmail.com",
                phone="+770644444444",
                password_hash=get_password_hash("admin123"),
                status=True
            ),
            UserModel(
                id=8,
                role_id=5,
                type_id=1,
                name="Весовщик Весовщиков",
                iin="555555555555",
                email="weigher@gmail.com",
                phone="+77065555555",
                password_hash=get_password_hash("admin123"),
                status=True
            ),
            UserModel(
                id=9,
                role_id=1,
                type_id=1,
                name="Система Цифровой Очереди",
                iin="100200300400",
                email="admin@gmail.com",
                phone="+77068495961",
                password_hash=get_password_hash("admin123"),
                status=True
            ),
        ]
        session.add_all(data)
        await session.commit()


async def add_organizations(session: Session):
    from app.domain.models.organization_model import OrganizationModel
    count_query = select(func.count()).select_from(OrganizationModel)
    total_items = await session.scalar(count_query)
    if total_items == 0:
        data = [
            OrganizationModel(
                id=1,
                full_name="ТОО 'KAZ ITECH'",
                short_name="KAZ ITECH",
                bin="230540028470",
                bik="BRKEKZKZ",
                kbe="KZ45914122203KZ00557",
                email="kazitech2023@gmail.com",
                phone="+77064205961",
                address="Астана Мангилик Ел",
                status=True,
                owner_id=2,
                type_id=1
            ),
            OrganizationModel(
                id=2,
                full_name="ТОО 'I-UNION'",
                short_name="I-UNION",
                bin="220640051457",
                bik="BRKEKZKG",
                kbe="KZ459141222034560557",
                email="iunion@gmail.com",
                phone="+77054171796",
                address="Астана Мангилик Ел",
                status=True,
                owner_id=3,
                type_id=1
            ),
        ]
        session.add_all(data)
        await session.commit()


async def add_vehicles(session: Session):
    from app.domain.models.vehicle_model import VehicleModel
    count_query = select(func.count()).select_from(VehicleModel)
    total_items = await session.scalar(count_query)
    if total_items == 0:
        data = [
            VehicleModel(
                document_number="34345DD34453",
                registration_number="ABC123",
                car_model="MAN",
                start_at=date(2024, 9, 17),
                vin="12345678912345678",
                produced_at=2023,
                engine_volume_sm=14000,
                weight_clean_kg=9000,
                weight_load_max_kg=20000,
                category_id=1,
                color_id=2,
                region_id=1,
                owner_id=1
            ),
            VehicleModel(
                document_number="34342HHHH453",
                registration_number="ABD546",
                car_model="METTLER TOLEDO",
                start_at=date(2024, 9, 17),
                vin="12345678912345899",
                produced_at=2023,
                engine_volume_sm=15000,
                weight_clean_kg=12000,
                weight_load_max_kg=31000,
                category_id=2,
                color_id=5,
                region_id=2,
                organization_id=1
            ),
            VehicleModel(
                document_number="34325GFDF453",
                registration_number="DVE543",
                car_model="MERCEDES ACTROS",
                start_at=date(2024, 9, 17),
                vin="12345678912345900",
                produced_at=2023,
                engine_volume_sm=15000,
                weight_clean_kg=11000,
                weight_load_max_kg=25000,
                category_id=3,
                color_id=8,
                region_id=17,
                organization_id=2
            ),
            VehicleModel(
                document_number="34345DDD453",
                registration_number="DDD859",
                car_model="KAMAZ",
                start_at=date(2024, 9, 17),
                vin="12398878912345678",
                produced_at=2023,
                engine_volume_sm=10000,
                weight_clean_kg=8000,
                weight_load_max_kg=18000,
                category_id=1,
                color_id=2,
                region_id=1,
                owner_id=4
            ),

        ]
        session.add_all(data)
        await session.commit()


async def add_workshop_schedules(session: Session):
    from app.domain.models.workshop_schedule_model import WorkshopScheduleModel
    count_query = select(func.count()).select_from(WorkshopScheduleModel)
    total_items = await session.scalar(count_query)
    if total_items == 0:
        data = [
            WorkshopScheduleModel(
                workshop_id=1,
                workshop_sap_id="5404",
                date_start=date(2024, 1, 1),
                date_end=date(2024, 12, 31),
                start_at=time(hour=9, minute=0, second=0, microsecond=0),
                end_at=time(hour=20, minute=0, second=0, microsecond=0),
                car_service_min=20,
                break_between_service_min=5,
                machine_at_one_time=4,
                is_active=True
            ),
            WorkshopScheduleModel(
                workshop_id=2,
                workshop_sap_id="5407",
                date_start=date(2024, 1, 1),
                date_end=date(2024, 12, 31),
                start_at=time(hour=9, minute=0, second=0, microsecond=0),
                end_at=time(hour=18, minute=0, second=0, microsecond=0),
                car_service_min=15,
                break_between_service_min=0,
                machine_at_one_time=2,
                is_active=True
            ),
        ]
        session.add_all(data)
        await session.commit()
