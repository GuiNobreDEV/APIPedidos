from decimal import Decimal

from sqlalchemy.orm import Session

from ..models.pedido import Pedido, PedidoStatus


class PedidoRepository:
    def __init__(self, db: Session):
        self.db = db

    def criar(
        self,
        cliente: str,
        produto: str,
        quantidade: int,
        valor_unitario: Decimal,
        valor_total: Decimal,
    ) -> Pedido:
        pedido = Pedido(
            cliente=cliente,
            produto=produto,
            quantidade=quantidade,
            valor_unitario=valor_unitario,
            valor_total=valor_total,
            status=PedidoStatus.CRIADO,
        )
        self.db.add(pedido)
        self.db.commit()
        self.db.refresh(pedido)
        return pedido

    def buscar_por_id(self, pedido_id: int) -> Pedido | None:
        return self.db.get(Pedido, pedido_id)

    def listar(self) -> list[Pedido]:
        return self.db.query(Pedido).order_by(Pedido.id).all()

    def atualizar_status(self, pedido: Pedido, novo_status: PedidoStatus) -> Pedido:
        pedido.status = novo_status
        self.db.commit()
        self.db.refresh(pedido)
        return pedido
