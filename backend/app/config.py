from pydantic_settings  import BaseSettings

class Settings(BaseSettings):
    postgres_user: str = "iot"
    postgres_password: str = "iot123"
    postgres_db: str = "iot"
    pgadmin_default_email: str = "admin@example.com"
    pgadmin_default_password: str = "admin"
    database_url: str = "postgresql://iot:iot123@127.0.0.1:5432/iot"

# Instanca postavki za dalje korišćenje
settings = Settings()
