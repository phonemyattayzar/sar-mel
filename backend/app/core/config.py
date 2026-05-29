from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str | None = None

    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str

    SECRET_KEY: str = "729df99824c0e68d0426b38466b0fdf12c0199e4e6669919f2a77a94bca42b49"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 11520  # 8 days in minutes


    class Config:
        env_file = ".env"
        extra = "ignore"   # 👈 IMPORTANT FIX


settings = Settings()