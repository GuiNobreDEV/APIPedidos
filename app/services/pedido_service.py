from decimal import Decimal, ROUND_HALF_UP

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from ..models.pedido import Pedido, PedidoStatus
from ..repositories.pedido_repository import PedidoRepository
from ..schemas.pedido import PedidoCreate


TRANSICOES_PERMITIDAS: dict[PedidoStatus, set[PedidoStatus]] = {
    PedidoStatus.CRIADO: {PedidoStatus.CONFIRMADO, PedidoStatus.CANCELADO},
    PedidoStatus.CONFIRMADO: {PedidoStatus.CANCELADO},
    PedidoStatus.CANCELADO: set(),
}


class PedidoService:
    def __init__(self, db: Session):
        self.repo = PedidoRepository(db)

    @staticmethod
    def calcular_valor_total(quantidade: int, valor_unitario: Decimal) -> Decimal:
        total = Decimal(quantidade) * Decimal(valor_unitario)
        return total.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

    def criar(self, dados: PedidoCreate) -> Pedido:
        valor_total = self.calcular_valor_total(dados.quantidade, dados.valor_unitario)
        return self.repo.criar(
            cliente=dados.cliente,
            produto=dados.produto,
            quantidade=dados.quantidade,
            valor_unitario=dados.valor_unitario,
            valor_total=valor_total,
        )

    def buscar(self, pedido_id: int) -> Pedido:
        pedido = self.repo.buscar_por_id(pedido_id)
        if pedido is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Pedido {pedido_id} não encontrado.",
            )
        return pedido

    def listar(self) -> list[Pedido]:
        return self.repo.listar()

    def alterar_status(self, pedido_id: int, novo_status: PedidoStatus) -> Pedido:
        pedido = self.buscar(pedido_id)

        if pedido.status == novo_status:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"O pedido {pedido_id} já está com o status {novo_status.value}.",
            )

        permitidos = TRANSICOES_PERMITIDAS[pedido.status]
        if novo_status not in permitidos:
            destinos = ", ".join(sorted(status_.value for status_ in permitidos))
            mensagem = (
                f"Não é possível alterar o pedido {pedido_id} de "
                f"{pedido.status.value} para {novo_status.value}."
            )
            if destinos:
                mensagem += f" Transições permitidas: {destinos}."
            else:
                mensagem += " O pedido não possui transições permitidas."
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=mensagem)

        return self.repo.atualizar_status(pedido, novo_status)
