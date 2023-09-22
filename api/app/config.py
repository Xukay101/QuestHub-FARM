from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    APP_NAME: str = "QuestHub API"

    ALGORITHM_TOKEN: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30 # 30 minutes
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7 # 7 days

    # Getting .env variables
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding='utf-8',
        extra='ignore'
    )

    # Frontend URL
    CLIENT_URL: str

    # Declared .env variables
    MONGODB_URI: str
    MONGODB_NAME: str

    JWT_SECRET_KEY: str # $ openssl rand -base64 24
    JWT_REFRESH_SECRET_KEY: str


settings = Settings()
