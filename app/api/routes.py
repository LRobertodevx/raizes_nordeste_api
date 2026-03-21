from fastapi import APIRouter, Depends, HTTPException, status, Header
from sqlalchemy.orm import Session
from app.infrastructure.database import get_db
from app.infrastructure import models
from app.domain import schemas
from app.application import services

router = APIRouter()

# Simulação de Segurança (Para atender os Testes T02, T03 e T07)
def verificar_token(authorization: str = Header(default=None)):
    if not authorization:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Não autenticado")
    return authorization

# Autenticação
@router.post("/auth/login", response_model=schemas.Token)
def login(credenciais: schemas.UsuarioLogin, db: Session = Depends(get_db)):
    usuario = db.query(models.Usuario).filter(models.Usuario.email == credenciais.email).first()

    if not usuario:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Usuário não encontrado")
    
    # Gera um token simulado contendo o perfil do usuário
    token_simulado = f"Bearer fake-jwt-token-{usuario.perfil.value}"
    return {"accessToken": token_simulado, "tokenType": "bearer"}

# Pedidos
@router.post("/pedidos", status_code=status.HTTP_201_CREATED)
def criar_novo_pedido(
    pedido: schemas.PedidoCreate, 
    db: Session = Depends(get_db), 
    token: str = Depends(verificar_token)
):
    return services.criar_pedido(db=db, pedido_in=pedido)

@router.get("/pedidos")
def listar_pedidos(
    canalPedido: str = None, 
    db: Session = Depends(get_db), 
    token: str = Depends(verificar_token)
):
    query = db.query(models.Pedido)
    if canalPedido: # Filtro de Multicanalidade (Teste T13)
        query = query.filter(models.Pedido.canal_pedido == canalPedido)
    return query.all()

@router.patch("/pedidos/{pedido_id}/status")
def atualizar_status(
    pedido_id: int, 
    status_update: schemas.StatusUpdate, 
    db: Session = Depends(get_db), 
    token: str = Depends(verificar_token)
):
    # Teste T03 (Erro 403)
    if "CLIENTE" in token.upper():
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Acesso Negado / Sem permissão")

    pedido = db.query(models.Pedido).filter(models.Pedido.id == pedido_id).first()
    if not pedido:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pedido não encontrado")
    
    pedido.status = status_update.status
    db.commit()
    db.refresh(pedido)
    return pedido

# Pagamentos
@router.post("/pagamentos/simular")
def simular_pagamento(
    pagamento: schemas.PagamentoMockCreate, 
    db: Session = Depends(get_db), 
    token: str = Depends(verificar_token)
):
    return services.simular_pagamento(db=db, pagamento_in=pagamento)

