from typing import Annotated

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from ..database import get_db
from ..schemas.pedido import PedidoCreate, PedidoOut, PedidoStatusUpdate
from ..services.pedido_service import PedidoService

router = APIRouter(prefix="/pedidos", tags=["pedidos"])


@router.post("", response_model=PedidoOut, status_code=status.HTTP_201_CREATED)
def create_pedido(
    pedido: PedidoCreate,
    db: Annotated[Session, Depends(get_db)],
):
    return PedidoService(db).criar(pedido)


@router.get("", response_model=list[PedidoOut])
def list_pedidos(db: Annotated[Session, Depends(get_db)]):
    return PedidoService(db).listar()


@router.get("/{pedido_id}", response_model=PedidoOut)
def get_pedido(pedido_id: int, db: Annotated[Session, Depends(get_db)]):
    return PedidoService(db).buscar(pedido_id)


@router.patch("/{pedido_id}/status", response_model=PedidoOut)
def update_status(
    pedido_id: int,
    dados: PedidoStatusUpdate,
    db: Annotated[Session, Depends(get_db)],
):
    return PedidoService(db).alterar_status(pedido_id, dados.status)
