from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "GalaxyMovil ERP API"
    environment: str = "development"
    api_prefix: str = "/api/v1"
    jwt_secret_key: str = "change-me-in-production"
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 120
    sqlserver_host: str = "localhost"
    sqlserver_port: int = 1433
    sqlserver_database: str = "POS_SYSTEM"
    sqlserver_user: str = "sa"
    sqlserver_password: str = "your_password"
    sqlserver_driver: str = "ODBC Driver 18 for SQL Server"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    @property
    def sqlserver_url(self) -> str:
        driver = self.sqlserver_driver.replace(" ", "+")
        
        host_part = self.sqlserver_host
        if self.sqlserver_port and "\\" not in self.sqlserver_host:
            # Solo usar puerto si no es una instancia con nombre como SERVER\SQLEXPRESS
            host_part = f"{self.sqlserver_host}:{self.sqlserver_port}"
            
        if self.sqlserver_user and self.sqlserver_password:
            return (
                f"mssql+pyodbc://{self.sqlserver_user}:{self.sqlserver_password}"
                f"@{host_part}/{self.sqlserver_database}"
                f"?driver={driver}&TrustServerCertificate=yes"
            )
        else:
            # Autenticación de Windows
            return (
                f"mssql+pyodbc://@{host_part}/{self.sqlserver_database}"
                f"?driver={driver}&Trusted_Connection=yes&TrustServerCertificate=yes"
            )


@lru_cache
def get_settings() -> Settings:
    return Settings()
