def assign_roles_to_route(app, path, roles):
    for route in app.routes:
        if route.path == path:
            if hasattr(route, 'roles'):
                route.roles.extend(roles)
            else:
                route.roles = roles


def assign_roles(app):
    # Назначаем роль "admin" для всех маршрутов
    assign_roles_to_route(app, "/role/", ["admin"])
    assign_roles_to_route(app, "/role/create", ["admin"])
    assign_roles_to_route(app, "/role/get_by_id/{id}", ["admin"])
    assign_roles_to_route(app, "/role/get_first", ["admin"])
    assign_roles_to_route(app, "/role/update/{id}", ["admin"])
    assign_roles_to_route(app, "/role/delete/{id}", ["admin"])

    assign_roles_to_route(app, "/user-type/", ["admin"])
    assign_roles_to_route(app, "/user-type/create", ["admin"])
    assign_roles_to_route(app, "/user-type/get_by_id/{id}", ["admin"])
    assign_roles_to_route(app, "/user-type/get_first", ["admin"])
    assign_roles_to_route(app, "/user-type/update/{id}", ["admin"])
    assign_roles_to_route(app, "/user-type/delete/{id}", ["admin"])

    assign_roles_to_route(app, "/user/create", ["admin"])
    assign_roles_to_route(app, "/user/update/{id}", ["admin"])
    assign_roles_to_route(app, "/user/all", ["admin"])
    assign_roles_to_route(app, "/user/get/{id}", ["admin"])
    assign_roles_to_route(app, "/user/get-by-iin/{iin}", ["admin"])
    assign_roles_to_route(app, "/user/get-by-email/{email}", ["admin"])
    assign_roles_to_route(app, "/user/get-by-phone/{phone}", ["admin"])
    assign_roles_to_route(app, "/user/delete/{id}", ["admin"])

    assign_roles_to_route(app, "/organization-type/", ["admin"])
    assign_roles_to_route(app, "/organization-type/create", ["admin"])
    assign_roles_to_route(app, "/organization-type/get_by_id/{id}", ["admin"])
    assign_roles_to_route(app, "/organization-type/update/{id}", ["admin"])
    assign_roles_to_route(app, "/organization-type/delete/{id}", ["admin"])

    assign_roles_to_route(app, "/organization/all", ["admin"])
    assign_roles_to_route(app, "/organization/get/{id}", ["admin"])
    assign_roles_to_route(app, "/organization/get_by_bin/{bin}", ["admin"])
    assign_roles_to_route(app, "/organization/create", ["admin"])
    assign_roles_to_route(app, "/organization/update/{id}", ["admin"])
    assign_roles_to_route(app, "/organization/delete/{id}", ["admin"])

    assign_roles_to_route(app, "/organization-employee/", ["admin"])
    assign_roles_to_route(app, "/organization-employee/get/{id}", ["admin"])
    assign_roles_to_route(app, "/organization-employee/create", ["admin"])
    assign_roles_to_route(app, "/organization-employee/update/{id}", ["admin"])
    assign_roles_to_route(app, "/organization-employee/delete/{id}", ["admin"])

    assign_roles_to_route(app, "/vehicle-color/", ["admin"])
    assign_roles_to_route(app, "/vehicle-color/create", ["admin"])
    assign_roles_to_route(app, "/vehicle-color/get_by_id/{id}", ["admin"])
    assign_roles_to_route(app, "/vehicle-color/update/{id}", ["admin"])
    assign_roles_to_route(app, "/vehicle-color/delete/{id}", ["admin"])

    assign_roles_to_route(app, "/vehicle-category/", ["admin"])
    assign_roles_to_route(app, "/vehicle-category/create", ["admin"])
    assign_roles_to_route(app, "/vehicle-category/get_by_id/{id}", ["admin"])
    assign_roles_to_route(app, "/vehicle-category/update/{id}", ["admin"])
    assign_roles_to_route(app, "/vehicle-category/delete/{id}", ["admin"])

    assign_roles_to_route(app, "/region/", ["admin"])
    assign_roles_to_route(app, "/region/create", ["admin"])
    assign_roles_to_route(app, "/region/get_by_id/{id}", ["admin"])
    assign_roles_to_route(app, "/region/update/{id}", ["admin"])
    assign_roles_to_route(app, "/region/delete/{id}", ["admin"])

    assign_roles_to_route(app, "/vehicle/", ["admin"])
    assign_roles_to_route(app, "/vehicle/create", ["admin"])
    assign_roles_to_route(app, "/vehicle/add-vehicle", ["admin"])
    assign_roles_to_route(app, "/vehicle/get/{id}", ["admin"])
    assign_roles_to_route(app, "/vehicle/get-own-cars", ["admin"])
    assign_roles_to_route(app, "/vehicle/get-organization-cars/{organization_id}", ["admin"])
    assign_roles_to_route(app, "/vehicle/update/{id}", ["admin"])
    assign_roles_to_route(app, "/vehicle/delete/{id}", ["admin"])

    assign_roles_to_route(app, "/factory/", ["admin"])
    assign_roles_to_route(app, "/factory/create", ["admin"])
    assign_roles_to_route(app, "/factory/get/{id}", ["admin"])
    assign_roles_to_route(app, "/factory/get_by_sap/{sap_id}", ["admin"])
    assign_roles_to_route(app, "/factory/update/{id}", ["admin"])
    assign_roles_to_route(app, "/factory/delete/{id}", ["admin"])

    assign_roles_to_route(app, "/workshop/", ["admin"])
    assign_roles_to_route(app, "/workshop/create", ["admin"])
    assign_roles_to_route(app, "/workshop/get/{id}", ["admin"])
    assign_roles_to_route(app, "/workshop/get_by_sap/{sap_id}", ["admin"])
    assign_roles_to_route(app, "/workshop/update/{id}", ["admin"])
    assign_roles_to_route(app, "/workshop/delete/{id}", ["admin"])

    assign_roles_to_route(app, "/material/", ["admin"])
    assign_roles_to_route(app, "/material/create", ["admin"])
    assign_roles_to_route(app, "/material/get/{id}", ["admin"])
    assign_roles_to_route(app, "/material/get_by_sap/{sap_id}", ["admin"])
    assign_roles_to_route(app, "/material/update/{id}", ["admin"])
    assign_roles_to_route(app, "/material/delete/{id}", ["admin"])

    assign_roles_to_route(app, "/auth/register", ["admin", "client"])
    assign_roles_to_route(app, "/auth/login", ["admin", "client"])
    assign_roles_to_route(app, "/auth/me", ["admin", "client"])

    assign_roles_to_route(app, "/order/get-all-order", ["admin", "client"])
    assign_roles_to_route(app, "/order/get-detail-order", ["admin", "client"])
    assign_roles_to_route(app, "/order/get-detail-schedule/{order_id}", ["admin", "client"])
    assign_roles_to_route(app, "/order/get-detail-schedule-history/{schedule_id}", ["admin", "client"])
    assign_roles_to_route(app, "/order/create-individual-order", ["admin", "client"])
    assign_roles_to_route(app, "/order/create-legal-order", ["admin", "client"])

    assign_roles_to_route(app, "/sap-request/recreate/{order_id}", ["admin"])

    assign_roles_to_route(app, "/kaspi/check", ["admin"])
    assign_roles_to_route(app, "/kaspi/pay", ["admin"])

    assign_roles_to_route(app, "/operation/", ["admin"])
    assign_roles_to_route(app, "/operation/create", ["admin"])
    assign_roles_to_route(app, "/operation/get_by_id/{id}", ["admin"])
    assign_roles_to_route(app, "/operation/update/{id}", ["admin"])
    assign_roles_to_route(app, "/operation/delete/{id}", ["admin"])

    assign_roles_to_route(app, "/workshop-schedule/", ["admin"])
    assign_roles_to_route(app, "/workshop-schedule/create", ["admin"])
    assign_roles_to_route(app, "/workshop-schedule/get_by_id/{id}", ["admin"])
    assign_roles_to_route(app, "/workshop-schedule/update/{id}", ["admin"])
    assign_roles_to_route(app, "/workshop-schedule/delete/{id}", ["admin"])

    assign_roles_to_route(app, "/schedule/create-individual", ["admin"])
    assign_roles_to_route(app, "/schedule/create-legal", ["admin"])
    assign_roles_to_route(app, "/schedule/get_schedule", ["admin"])
    assign_roles_to_route(app, "/schedule/get-active-schedules", ["admin"])
    assign_roles_to_route(app, "/schedule/get-canceled-schedules", ["admin"])

    assign_roles_to_route(app, "/schedule-history/take-request/{schedule_id}", ["admin"])
    assign_roles_to_route(app, "/schedule-history/make-decision/{schedule_id}", ["admin"])

    assign_roles_to_route(app, "/get-qr/get-qr-link/{order_id}", ["admin", "client"])

    assign_roles_to_route(app, "/test/test", ["admin"])

