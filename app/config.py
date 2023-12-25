import logging
import os
from dataclasses import dataclass

logging.basicConfig(level=logging.INFO)


@dataclass
class Settings:
    PROJECT_NAME: str = "we-are-being-watched"

    DB_CONFIG = os.getenv(
        "DB_CONFIG",
        "postgresql+asyncpg://{}:{}@{}/{}".format(
            os.getenv("DB_USER", "postgres"),
            os.getenv("DB_PASSWORD", "postgres"),
            os.getenv("DB_HOST", "postgres:5432"),
            os.getenv("DB_NAME", "you-are-being-watched"),
        ),
    )

    TEST_DB_CONFIG = os.getenv(
        "DB_CONFIG",
        "postgresql+asyncpg://{}:{}@{}/{}".format(
            os.getenv("DB_USER", "postgres"),
            os.getenv("DB_PASSWORD", "postgres"),
            os.getenv("DB_HOST", "postgres:5432"),
            "test",
        ),
    )

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
