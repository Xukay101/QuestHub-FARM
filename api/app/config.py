from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_name: str = "QuestHub API"

    # Getting .env variables
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding='utf-8',
        extra='ignore'
    )

    # Declared .env variables
    DATABASE_URI: str
    DATABASE_NAME: str

    JWT_SECRET_KEY: str # $ openssl rand -base64 24

settings = Settings()