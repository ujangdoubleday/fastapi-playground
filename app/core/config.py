from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    PROJECT_NAME: str = "FastAPI Playground"
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # OS environment variables take precedence over .env file
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
