from fastapi.responses import HTMLResponse
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.openapi.utils import get_openapi


def custom_openapi(app, role: str):
    routes = [route for route in app.routes if hasattr(route, 'roles') and role in route.roles]
    openapi_schema = get_openapi(
        title=f"DIGITAL QUEUE TEST - {role.capitalize()}",
        version="0.1",
        description=f"Документация для {role}",
        routes=routes,
    )
    return openapi_schema


def setup_documentation(app):
    # Главная страница с выбором ролей
    @app.get("/docs", include_in_schema=False)
    async def get_roles_page():
        html_content = """
        <html>
            <head>
                <title>API Documentation by Roles</title>
                <style>
                    body {
                        font-family: Arial, sans-serif;
                        background-color: #f4f4f9;
                        margin: 0;
                        padding: 0;
                        display: flex;
                        justify-content: center;
                        align-items: center;
                        height: 100vh;
                    }
                    .container {
                        text-align: center;
                        background-color: white;
                        padding: 30px;
                        border-radius: 10px;
                        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
                    }
                    h1 {
                        color: #333;
                        margin-bottom: 20px;
                    }
                    ul {
                        list-style-type: none;
                        padding: 0;
                    }
                    li {
                        margin: 30px 0;
                    }
                    a {
                        text-decoration: none;
                        font-size: 18px;
                        color: white;
                        background-color: #4CAF50;
                        padding: 10px 20px;
                        border-radius: 5px;
                        transition: background-color 0.3s ease;
                    }
                    a:hover {
                        background-color: #45a049;
                    }
                </style>
            </head>
            <body>
                <div class="container">
                    <h1>Выбор документации API по роли</h1>
                    <ul>
                        <li><a target="_blank" href="/docs/admin">Администратор</a></li>
                        <li><a target="_blank" href="/docs/client">Клиент</a></li>
                    </ul>
                </div>
            </body>
        </html>
        """
        return HTMLResponse(content=html_content)

    # Swagger UI для каждой роли
    @app.get("/docs/admin", include_in_schema=False)
    async def get_admin_docs():
        return get_swagger_ui_html(openapi_url="/openapi/admin", title="Admin Docs")

    @app.get("/docs/client", include_in_schema=False)
    async def get_user_docs():
        return get_swagger_ui_html(openapi_url="/openapi/client", title="Client Docs")

    # OpenAPI схемы для каждой роли
    @app.get("/openapi/admin", include_in_schema=False)
    async def get_admin_openapi():
        return custom_openapi(app, "admin")

    @app.get("/openapi/client", include_in_schema=False)
    async def get_user_openapi():
        return custom_openapi(app, "client")
