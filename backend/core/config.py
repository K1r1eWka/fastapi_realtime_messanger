from pydantic_settings import BaseSettings, SettingsConfigDict

class DataBaseSettings(BaseSettings):
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_SERVER: str
    POSTGRES_PORT: int
    POSTGRES_NAME: str

    model_config = SettingsConfigDict(
        # from which file load configuration
        env_file="./.env",
        # we will ignor empty fields, for instance if in our setting will be one more field but we dont define this field in model, that mean that we will ignore this field in our settings, but dont run any execution 
        env_ignore_empty=True,
        # we will ignore extra fields witch we do not need
        extra="ignore"
    )

class SecuritySettings(BaseSettings):
    JWT_SECRET: str
    JWT_ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    model_config = SettingsConfigDict(
        env_file="./.env",
        env_ignore_empty=True,
        extra="ignore",
    )

db_settings = DataBaseSettings()
security_settings = SecuritySettings()