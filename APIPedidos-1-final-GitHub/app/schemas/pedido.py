from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field, condecimal, field_validator

from ..models.pedido import PedidoStatus

DecimalType = condecimal(max_digits=14, decimal_places=2)


class PedidoCreate(BaseModel):
    cliente: str = Field(min_length=1, max_length=150)
    produto: str = Field(min_length=1, max_length=150)
    quantidade: int = Field(gt=0)
    valor_unitario: DecimalType = Field(gt=0)  # type: ignore

    @field_validator("cliente", "produto")
    @classmethod
    def remover_espacos_externos(cls, valor: str) -> str:
        valor = valor.strip()
        if not valor:
            raise ValueError("O campo não pode ser vazio.")
        return valor


class PedidoStatusUpdate(BaseModel):
    status: PedidoStatus


class PedidoOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    cliente: str
    produto: str
    quantidade: int
    valor_unitario: DecimalType  # type: ignore
    valor_total: DecimalType  # type: ignore
    status: PedidoStatus
    data_criacao: datetime
