from pydantic import BaseSettings


class Settings(BaseSettings):
    DB_USER: str
    DB_PASS: str
    DB_HOST: str
    DB_NAME: str

    class Config:
        env_file = ".env"


settings = Settings()
