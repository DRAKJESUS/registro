import os
from dotenv import load_dotenv

load_dotenv()

def get_env(key: str, required: bool = True):
    value = os.getenv(key)
    if required and not value:
        raise ValueError(f"Falta la variable de entorno: {key}")
    return value

POSTGRES_USER = get_env("POSTGRES_USER")
POSTGRES_PASSWORD = get_env("POSTGRES_PASSWORD")
POSTGRES_HOST = get_env("POSTGRES_HOST")
POSTGRES_PORT = get_env("POSTGRES_PORT")
POSTGRES_DB = get_env("POSTGRES_DB")

DATABASE_URL = (
    f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@"
    f"{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
)
