import os
from dotenv import load_dotenv

# Cargar variables de entorno desde .env
load_dotenv()

# Debug temporal para verificar valores en Render
print("DEBUG CONFIG:")
print("DB_USER:", os.getenv("POSTGRES_USER"))
print("DB_PASS:", os.getenv("POSTGRES_PASSWORD"))
print("DB_HOST:", os.getenv("POSTGRES_HOST"))
print("DB_PORT:", os.getenv("POSTGRES_PORT"))
print("DB_NAME:", os.getenv("POSTGRES_DB"))

# Asignación de variables
DB_USER = os.getenv("POSTGRES_USER")
DB_PASS = os.getenv("POSTGRES_PASSWORD")
DB_HOST = os.getenv("POSTGRES_HOST")
DB_PORT = os.getenv("POSTGRES_PORT")
DB_NAME = os.getenv("POSTGRES_DB")

# URL de conexión con asyncpg para SQLAlchemy 2.x
DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
