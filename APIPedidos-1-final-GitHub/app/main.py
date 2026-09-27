from contextlib import asynccontextmanager

from fastapi import FastAPI # type: ignore

from .api import pedidos
from .database import Base, engine, wait_for_database


@asynccontextmanager
async def lifespan(app: FastAPI):
    wait_for_database()
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title="API de Pedidos",
    version="1.0.0",
    description="API REST para cadastro e gerenciamento de pedidos.",
    lifespan=lifespan,
)

app.include_router(pedidos.router)


@app.get("/health", tags=["infra"])
def health():
    return {"status": "ok"}
