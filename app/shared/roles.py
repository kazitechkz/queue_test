def assign_roles(app):
    # Admin Roles
    admin_prefixes = [
        "/auth",
        "/role",
        "/user",
        "/user-type",
        "/organization-type",
        "/organization",
        "/organization-employee",
        "/vehicle-color",
        "/vehicle-category",
        "/region",
        "/vehicle",
        "/factory",
        "/workshop",
        "/material",
        "/order",
        "/sap-request",
        "/operation",
        "/workshop-schedule"
    ]
    for prefix in admin_prefixes:
        assign_role(app, "admin", prefix)

    # Client Roles
    client_prefixes = [
        "/kaspi",
        "/schedule",
        "/schedule-history"
    ]
    for prefix in client_prefixes:
        assign_role(app, "client", prefix)


def assign_role(app, role: str, prefix: str):
    for route in app.routes:
        if route.path.startswith(prefix):
            route.role = role  # Присваиваем роль маршрутам
