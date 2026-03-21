from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.infrastructure import models
from app.domain import schemas

def criar_pedido(db: Session, pedido_in: schemas.PedidoCreate):
    # Verifica se a unidade existe
    unidade = db.query(models.Unidade).filter(models.Unidade.id == pedido_in.unidade_id).first()
    if not unidade:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Unidade não encontrada.")

    total_pedido = 0.0
    itens_para_salvar = []
    estoques_para_atualizar = []

    # Valida o estoque de cada item e calcula o total
    for item in pedido_in.itens:
        produto = db.query(models.Produto).filter(models.Produto.id == item.produto_id).first()
        if not produto:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Produto ID {item.produto_id} não encontrado.")

        estoque = db.query(models.Estoque).filter(
            models.Estoque.unidade_id == pedido_in.unidade_id,
            models.Estoque.produto_id == item.produto_id
        ).first()

        # Regra do cenário T07 do PDF: Erro 409 - falta de estoque
        if not estoque or estoque.quantidade < item.quantidade:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Estoque insuficiente para o produto {produto.nome}. Disponível: {estoque.quantidade if estoque else 0}"
            )

        # Prepara os valores
        total_pedido += produto.preco * item.quantidade
        itens_para_salvar.append({
            "produto_id": produto.id,
            "quantidade": item.quantidade,
            "preco_unitario": produto.preco
        })
        estoques_para_atualizar.append((estoque, item.quantidade))

    # Cria o pedido raiz no banco de dados
    novo_pedido = models.Pedido(
        unidade_id=pedido_in.unidade_id,
        canal_pedido=pedido_in.canal_pedido,
        status=models.StatusPedidoEnum.AGUARDANDO_PAGAMENTO,
        total=total_pedido
    )
    db.add(novo_pedido)
    db.flush() 

    # Salva os itens e debita o estoque
    for item_data in itens_para_salvar:
        novo_item = models.ItemPedido(pedido_id=novo_pedido.id, **item_data)
        db.add(novo_item)

    for estoque_obj, qtd in estoques_para_atualizar:
        estoque_obj.quantidade -= qtd

    # Efetiva a transação no banco
    db.commit()
    db.refresh(novo_pedido)
    return novo_pedido


def simular_pagamento(db: Session, pagamento_in: schemas.PagamentoMockCreate):
    pedido = db.query(models.Pedido).filter(models.Pedido.id == pagamento_in.pedido_id).first()
    if not pedido:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pedido não encontrado.")

    if pedido.status != models.StatusPedidoEnum.AGUARDANDO_PAGAMENTO:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Este pedido não está aguardando pagamento.")

    status_transacao = "RECUSADO" if pagamento_in.forma_pagamento.upper() == "ERRO" else "APROVADO"

    novo_pagamento = models.PagamentoMock(
        pedido_id=pedido.id,
        forma_pagamento=pagamento_in.forma_pagamento,
        status_mock=status_transacao
    )
    db.add(novo_pagamento)

    # Avança o status do pedido se aprovado (Cenário T09 e T10 do PDF)
    if status_transacao == "APROVADO":
        pedido.status = models.StatusPedidoEnum.COZINHA

    db.commit()
    db.refresh(novo_pagamento)
    
    # Se recusado, devolve erro 400 (Cenário T11 do PDF)
    if status_transacao == "RECUSADO":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Pagamento recusado pelo gateway externo.")
        
    return novo_pagamento