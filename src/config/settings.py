from pathlib import Path
from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict

PROJECT_ROOT = Path(__file__).parent.parent.resolve()


class Settings(BaseSettings):
    db_host: str = "localhost"
    db_port: str = "3306"
    db_user: str = "root"
    db_password: Optional[str] = None
    db_database: str = "insu"

    vector_path: str = "insu_data"
    openai_api_key: Optional[str] = None
    upstage_api_key: Optional[str] = None

    model_config = SettingsConfigDict(env_file=f"{PROJECT_ROOT}/.env", env_file_encoding="utf-8")


settings = Settings()
