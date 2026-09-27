import os
import time

from sqlalchemy import create_engine, text
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise RuntimeError("A variável de ambiente DATABASE_URL não foi definida.")

engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def wait_for_database(retries: int = 30, delay: float = 2.0) -> None:
    last_error = None
    for _ in range(retries):
        try:
            with engine.connect() as connection:
                connection.execute(text("SELECT 1"))
            return
        except Exception as exc:  # banco pode ainda estar inicializando
            last_error = exc
            time.sleep(delay)
    raise RuntimeError("Não foi possível conectar ao PostgreSQL.") from last_error
