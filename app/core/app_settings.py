from dotenv import load_dotenv
from pydantic_settings import BaseSettings


load_dotenv()


class AppSettings(BaseSettings):
    APP_DATABASE: str

    PG_CONNECTION: str
    PG_DB_HOST: str
    PG_DB_PORT: str
    PG_DB_USER: str
    PG_DB_PASSWORD: str
    PG_DB_NAME: str

    MYSQL_CONNECTION: str
    MYSQL_DB_HOST: str
    MYSQL_DB_PORT: str
    MYSQL_DB_USER: str
    MYSQL_DB_PASSWORD: str
    MYSQL_DB_NAME: str

    DB_POOL_SIZE:int
    DB_MAX_OVERFLOW:int
    DB_POOL_TIMEOUT:int
    DB_POOL_RECYCLE:int

    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    REFRESH_TOKEN_EXPIRE_DAYS: int
    APP_STATUS: str

    KEYCLOAK_SERVER_URL:str
    KEYCLOAK_REALM:str
    KEYCLOAK_CLIENT_ID:str
    KEYCLOAK_CLIENT_SECRET:str

    @property
    def DB_URL_ASYNC(self) -> str:
        if self.APP_DATABASE == "postgresql":
            return f"{self.PG_CONNECTION}://{self.PG_DB_USER}:{self.PG_DB_PASSWORD}@{self.PG_DB_HOST}:{self.PG_DB_PORT}/{self.PG_DB_NAME}"
        return f"{self.MYSQL_CONNECTION}://{self.MYSQL_DB_USER}:{self.MYSQL_DB_PASSWORD}@{self.MYSQL_DB_HOST}:{self.MYSQL_DB_PORT}/{self.MYSQL_DB_NAME}"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


app_settings = AppSettings()
