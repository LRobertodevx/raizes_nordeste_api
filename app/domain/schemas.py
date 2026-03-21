from pydantic import BaseModel, Field
from typing import List
from app.infrastructure.models import CanalEnum, StatusPedidoEnum

# 1. Contratos de Autenticação
class UsuarioLogin(BaseModel):
    email: str
    senha: str

class Token(BaseModel):
    access_token: str = Field(alias="accessToken")
    token_type: str = Field(alias="tokenType")

#2. Contratos de Criação de Pedido (Entrada)
class ItemPedidoCreate(BaseModel):
    produto_id: int = Field(alias="produtoId")
    quantidade: int = Field(gt=0, description="A quantidade deve ser maior que zero")

class PedidoCreate(BaseModel):
    unidade_id: int = Field(alias="unidadeId")
    # No Python é canal_pedido, no JSON exigido é canalPedido. Conforme explicitado > 2.2 REQUISITO DE DOMÍNIO – MULTICANALIDADE
    canal_pedido: CanalEnum = Field(alias="canalPedido")
    itens: List[ItemPedidoCreate]
    forma_pagamento: str = Field(alias="formaPagamento")

# 3. Contratos de Pagamento e Status
class PagamentoMockCreate(BaseModel):
    pedido_id: int = Field(alias="pedidoId")
    valor_total: float = Field(alias="valorTotal")
    forma_pagamento: str = Field(alias="formaPagamento")

class StatusUpdate(BaseModel):
    status: StatusPedidoEnum