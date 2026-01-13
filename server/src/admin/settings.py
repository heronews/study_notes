from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="", env_file=".env", env_file_encoding="utf-8"
    )
    db_url: str
    jwt_key: str
    jwt_algorithm: str


app_settings = Settings()
