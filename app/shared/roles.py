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
    assign_roles_to_route(app, "/role/update/{id}", ["admin"])
    assign_roles_to_route(app, "/role/delete/{id}", ["admin"])

    assign_roles_to_route(app, "/user-type/", ["admin", "client"])
    assign_roles_to_route(app, "/user-type/create", ["admin"])
    assign_roles_to_route(app, "/user-type/get-by-id/{id}", ["admin"])
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

    assign_roles_to_route(app, "/organization-type/", ["admin", "client"])
    assign_roles_to_route(app, "/organization-type/create", ["admin"])
    assign_roles_to_route(app, "/organization-type/get-by-id/{id}", ["admin"])
    assign_roles_to_route(app, "/organization-type/update/{id}", ["admin"])
    assign_roles_to_route(app, "/organization-type/delete/{id}", ["admin"])

    assign_roles_to_route(app, "/organization/all", ["admin"])
    assign_roles_to_route(app, "/organization/get/{id}", ["admin"])
    assign_roles_to_route(app, "/organization/get-by-bin/{bin}", ["admin"])
    assign_roles_to_route(app, "/organization/my-organizations", ["client"])
    assign_roles_to_route(app, "/organization/create", ["admin"])
    assign_roles_to_route(app, "/organization/update/{id}", ["admin"])
    assign_roles_to_route(app, "/organization/delete/{id}", ["admin"])

    assign_roles_to_route(app, "/organization-employee/", ["admin"])
    assign_roles_to_route(app, "/organization-employee/get/{id}", ["admin"])
    assign_roles_to_route(app, "/organization-employee/my-drivers/{organization_id}", ["client"])
    assign_roles_to_route(app, "/organization-employee/create", ["admin"])
    assign_roles_to_route(app, "/organization-employee/update/{id}", ["admin"])
    assign_roles_to_route(app, "/organization-employee/delete/{id}", ["admin"])

    assign_roles_to_route(app, "/employee-request/search-employee", ["client"])
    assign_roles_to_route(app, "/employee-request/create-request", ["client"])
    assign_roles_to_route(app, "/employee-request/my-requests", ["client"])
    assign_roles_to_route(app, "/employee-request/make-decision/{id}", ["client"])

    assign_roles_to_route(app, "/vehicle-color/", ["admin", "client"])
    assign_roles_to_route(app, "/vehicle-color/create", ["admin"])
    assign_roles_to_route(app, "/vehicle-color/get-by-id/{id}", ["admin"])
    assign_roles_to_route(app, "/vehicle-color/update/{id}", ["admin"])
    assign_roles_to_route(app, "/vehicle-color/delete/{id}", ["admin"])

    assign_roles_to_route(app, "/vehicle-category/", ["admin", "client"])
    assign_roles_to_route(app, "/vehicle-category/create", ["admin"])
    assign_roles_to_route(app, "/vehicle-category/get-by-id/{id}", ["admin"])
    assign_roles_to_route(app, "/vehicle-category/update/{id}", ["admin"])
    assign_roles_to_route(app, "/vehicle-category/delete/{id}", ["admin"])

    assign_roles_to_route(app, "/region/", ["admin", "client"])
    assign_roles_to_route(app, "/region/create", ["admin"])
    assign_roles_to_route(app, "/region/get-by-id/{id}", ["admin"])
    assign_roles_to_route(app, "/region/update/{id}", ["admin"])
    assign_roles_to_route(app, "/region/delete/{id}", ["admin"])

    assign_roles_to_route(app, "/vehicle/", ["admin"])
    assign_roles_to_route(app, "/vehicle/create", ["admin"])
    assign_roles_to_route(app, "/vehicle/add-vehicle", ["admin", "client"])
    assign_roles_to_route(app, "/vehicle/get/{id}", ["admin"])
    assign_roles_to_route(app, "/vehicle/get-own-cars", ["client"])
    assign_roles_to_route(app, "/vehicle/get-organization-cars/{organization_id}", ["client"])
    assign_roles_to_route(app, "/vehicle/update/{id}", ["admin"])
    assign_roles_to_route(app, "/vehicle/delete/{id}", ["admin"])

    assign_roles_to_route(app, "/factory/", ["admin", "client"])
    assign_roles_to_route(app, "/factory/create", ["admin"])
    assign_roles_to_route(app, "/factory/get/{id}", ["admin"])
    assign_roles_to_route(app, "/factory/get-by-sap/{sap_id}", ["admin", "employee", "client"])
    assign_roles_to_route(app, "/factory/update/{id}", ["admin"])
    assign_roles_to_route(app, "/factory/delete/{id}", ["admin"])

    assign_roles_to_route(app, "/workshop/", ["admin", "client"])
    assign_roles_to_route(app, "/workshop/create", ["admin"])
    assign_roles_to_route(app, "/workshop/get/{id}", ["admin"])
    assign_roles_to_route(app, "/workshop/get-by-sap/{sap_id}", ["admin"])
    assign_roles_to_route(app, "/workshop/update/{id}", ["admin"])
    assign_roles_to_route(app, "/workshop/delete/{id}", ["admin"])

    assign_roles_to_route(app, "/material/", ["admin", "client"])
    assign_roles_to_route(app, "/material/create", ["admin"])
    assign_roles_to_route(app, "/material/get/{id}", ["admin"])
    assign_roles_to_route(app, "/material/get-by-sap/{sap_id}", ["admin"])
    assign_roles_to_route(app, "/material/update/{id}", ["admin"])
    assign_roles_to_route(app, "/material/delete/{id}", ["admin"])

    assign_roles_to_route(app, "/auth/register", ["admin", "client", "employee"])
    assign_roles_to_route(app, "/auth/login", ["admin", "client", "employee"])
    assign_roles_to_route(app, "/auth/refresh", ["admin", "client", "employee"])
    assign_roles_to_route(app, "/auth/me", ["admin", "client", "employee"])

    assign_roles_to_route(app, "/order-status/all", ["admin", "client", "employee"])
    assign_roles_to_route(app, "/order-status/get/{id}", ["admin", "client", "employee"])
    assign_roles_to_route(app, "/order-status/get-by-value/{value}", ["admin", "client", "employee"])

    assign_roles_to_route(app, "/order/check-order-payment", ["admin"])
    assign_roles_to_route(app, "/order/get-all-order", ["admin", "client"])
    assign_roles_to_route(app, "/order/get-detail-order", ["admin", "client"])
    assign_roles_to_route(app, "/order/my-paid-orders", ["client"])
    assign_roles_to_route(app, "/order/create-individual-order", ["client"])
    assign_roles_to_route(app, "/order/create-legal-order", ["client"])

    assign_roles_to_route(app, "/sap-request/recreate/{order_id}", ["client"])

    assign_roles_to_route(app, "/kaspi/check", ["admin", "client"])
    assign_roles_to_route(app, "/kaspi/pay", ["admin", "client"])

    assign_roles_to_route(app, "/operation/", ["admin", "client"])
    assign_roles_to_route(app, "/operation/create", ["admin"])
    assign_roles_to_route(app, "/operation/get/{id}", ["admin"])
    assign_roles_to_route(app, "/operation/get-by-value/{value}", ["admin"])
    assign_roles_to_route(app, "/operation/update/{id}", ["admin"])
    assign_roles_to_route(app, "/operation/delete/{id}", ["admin"])

    assign_roles_to_route(app, "/workshop-schedule/", ["admin", "client", "employee"])
    assign_roles_to_route(app, "/workshop-schedule/create", ["admin"])
    assign_roles_to_route(app, "/workshop-schedule/get-by-id/{id}", ["admin", "client", "employee"])
    assign_roles_to_route(app, "/workshop-schedule/update/{id}", ["admin"])
    assign_roles_to_route(app, "/workshop-schedule/delete/{id}", ["admin"])

    assign_roles_to_route(app, "/schedule/create-individual", ["client"])
    assign_roles_to_route(app, "/schedule/create-legal", ["client"])
    assign_roles_to_route(app, "/schedule/get-schedule", ["admin", "client"])
    assign_roles_to_route(app, "/schedule/get-active-schedules", ["employee"])
    assign_roles_to_route(app, "/schedule/get-canceled-schedules", ["employee"])
    assign_roles_to_route(app, "/schedule/get-all-schedules", ["admin", "employee"])
    assign_roles_to_route(app, "/schedule/my-active-schedules", ["client"])
    assign_roles_to_route(app, "/schedule/my-schedules", ["client"])
    assign_roles_to_route(app, "/schedule/my-schedules-count", ["client"])
    assign_roles_to_route(app, "/schedule/reschedules-all", ["admin"])
    assign_roles_to_route(app, "/schedule/cancel-all-schedules", ["admin"])
    assign_roles_to_route(app, "/schedule/reschedule-to-date/{schedule_id}", ["admin"])
    assign_roles_to_route(app, "/schedule/cancel-one/{schedule_id}", ["admin"])
    assign_roles_to_route(app, "/schedule/get/{id}", ["admin", "client", "employee"])
    assign_roles_to_route(app, "/schedule/my-responsible-schedules", ["employee"])
    assign_roles_to_route(app, "/schedule/check-late-schedules", ["admin"])

    assign_roles_to_route(app, "/schedule-history/take-request/{schedule_id}", ["employee"])
    assign_roles_to_route(app, "/schedule-history/make-decision/{schedule_id}", ["employee"])

    assign_roles_to_route(app, "/act-weight/all", ["admin", "employee"])
    assign_roles_to_route(app, "/act-weight/get/{id}", ["admin", "employee", "client"])

    assign_roles_to_route(app, "/initial-weight/all", ["admin", "employee"])
    assign_roles_to_route(app, "/initial-weight/get/{id}", ["admin", "employee", "client"])
    assign_roles_to_route(app, "/baseline-weight/get-vehicle-trailer-weights", ["admin", "employee", "client"])
    assign_roles_to_route(app, "/baseline-weight/get/{vehicle-id}", ["admin", "employee", "client"])

    assign_roles_to_route(app, "/payment_document/upload-payment-file", ["client"])
    assign_roles_to_route(app, "/payment_document/get-payment-docs", ["employee"])
    assign_roles_to_route(app, "/payment_document/get-payment-doc-by-order-id/{order_id}", ["employee"])
    assign_roles_to_route(app, "/payment_document/add-comment-to-doc", ["employee"])
    assign_roles_to_route(app, "/payment_document/make-decision", ["employee"])

    assign_roles_to_route(app, "/get-qr/get-qr-link/{order_id}", ["admin", "client"])

    assign_roles_to_route(app, "/test/test", ["admin"])
