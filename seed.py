from sqlalchemy.orm import Session
import bcrypt
from app.infrastructure.database import SessionLocal, Base, engine
from app.infrastructure import models

def popular_banco():

    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        # Verifica se já tem usuários para não duplicar
        if db.query(models.Usuario).first():
            print("O banco já está populado! O Seed foi ignorado.")
            return

        print("Populando o banco de dados 'Raízes do Nordeste'...")

        # Cria Usuários - bcrypt
        senha_bytes = b"senha123"
        salt = bcrypt.gensalt()
        senha_hash = bcrypt.hashpw(senha_bytes, salt).decode('utf-8')
        
        cliente = models.Usuario(nome="João Cliente", email="cliente@teste.com", senha_hash=senha_hash, perfil=models.PerfilEnum.CLIENTE)
        gerente = models.Usuario(nome="Maria Gerente", email="gerente@teste.com", senha_hash=senha_hash, perfil=models.PerfilEnum.GERENTE)
        db.add_all([cliente, gerente])

        # Cria a Unidade
        unidade = models.Unidade(nome="Matriz - Raízes", endereco="Rua Principal, 100")
        db.add(unidade)
        db.flush() # Atualiza para pegar o ID gerado

        # Cria Produtos
        p1 = models.Produto(nome="Tapioca de Carne de Sol", preco=18.90)
        p2 = models.Produto(nome="Cuscuz com Queijo", preco=12.00)
        db.add_all([p1, p2])
        db.flush() 

        # Cria o Estoque
        estoque_1 = models.Estoque(unidade_id=unidade.id, produto_id=p1.id, quantidade=50)
        # BAIXO estoque para teste - Regra de Negócio (Erro 409)
        estoque_2 = models.Estoque(unidade_id=unidade.id, produto_id=p2.id, quantidade=2) 
        db.add_all([estoque_1, estoque_2])

        # Salva
        db.commit()
        print("✅ Seed concluído com sucesso! Usuários, Unidade, Produtos e Estoques criados.")

    except Exception as e:
        db.rollback()
        print(f"❌ Erro ao popular o banco: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    popular_banco()