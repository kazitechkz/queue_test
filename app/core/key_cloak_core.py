from keycloak import KeycloakOpenID

from app.core.app_settings import app_settings


keycloak_openid = KeycloakOpenID(
    server_url=app_settings.KEYCLOAK_SERVER_URL,
    realm_name=app_settings.KEYCLOAK_REALM,
    client_id=app_settings.KEYCLOAK_CLIENT_ID,
    client_secret_key=app_settings.KEYCLOAK_CLIENT_SECRET,
    verify=False  # Отключение проверки сертификатов
)

def get_openid_config():
    return keycloak_openid.well_known()