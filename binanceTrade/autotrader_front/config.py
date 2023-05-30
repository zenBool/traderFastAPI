import os

from pydantic import BaseSettings


class Settings(BaseSettings):
    app_name = os.getenv('NAME_APP')
    # db_url = os.getenv("DB_URI")

    class Config:
        env_file: str = '../.env'


settings = Settings()
