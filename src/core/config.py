import os
import logging


class Config:
    LOG_LEVEL = os.getenv("LOG_LEVEL", logging.getLevelName("INFO"))
    API_VERSION = os.getenv("API_VERSION", "v1")
    POSTGRES_HOST = os.getenv("POSTGRES_HOST")
    POSTGRES_USER = os.getenv("POSTGRES_USER")
    POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
    POSTGRES_DB = os.getenv("POSTGRES_DB")
    DATABASE_URL = os.environ.get("DATABASE_URL", "postgresql://myuser:mypass@localhost:5432/sprk")
