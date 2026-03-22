# 🌵 Raízes do Nordeste API - MVP

Bem-vindo ao Back-end do MVP "Raízes do Nordeste". Esta API RESTful foi desenvolvida com **FastAPI** e **SQLite** para gerenciar pedidos, controle de estoque multicanal e simulação de pagamentos, atendendo aos requisitos de arquitetura em camadas.

## 🚀 Tecnologias Utilizadas
* **Linguagem:** Python 3.13
* **Framework Web:** FastAPI
* **Banco de Dados:** SQLite + SQLAlchemy (ORM)
* **Validação de Dados:** Pydantic
* **Segurança:** Bcrypt (Hash de Senhas)
* **Servidor:** Uvicorn

## ⚙️ Como Rodar o Projeto Localmente

### 1. Pré-requisitos
Certifique-se de ter o Python 3.10+ instalado em sua máquina.

### 2. Clonar e Configurar o Ambiente
Abra o terminal e execute os seguintes comandos:

```bash
# Clone o repositório
git clone https://github.com/LRobertodevx/raizes_nordeste_api.git
cd raizes_nordeste_api

# Crie o ambiente virtual
python -m venv venv

# Ative o ambiente virtual:

    # No Windows (PowerShell):
    .\venv\Scripts\Activate.ps1

    # No Linux/Mac:
    source venv/bin/activate

# Instale as dependências
pip install -r requirements.txt
```

### 3. Variáveis de Ambiente (.env)
Crie um arquivo chamado `.env` na raiz do projeto e copie o conteúdo do arquivo `.env.example` para dentro dele.
(Nota: O banco de dados SQLite será gerado automaticamente neste caminho).

### 4. Popular o Banco de Dados (Seed e Migrations)
O nosso script de seed já está configurado para atuar como uma Migration inicial, criando as tabelas automaticamente antes de inserir os dados. Execute:

```bash
python seed.py
```
(Você verá a mensagem: "✅ Seed concluído com sucesso!")

### 5. Iniciar o Servidor
Execute o comando abaixo para ligar a API:

```bash
uvicorn main:app --reload
```
> A API estará rodando no endereço: http://localhost:8000

# 📖 Documentação e Testes

### Swagger UI (Visualização Interativa)

Com o servidor rodando, acesse a documentação oficial gerada automaticamente pelo FastAPI:

> 👉 http://localhost:8000/docs

### Coleção Postman / Insomnia

Na raiz deste projeto, você encontrará o arquivo ```collection_testes.json.```
<br>
Ele contém **13 cenários de testes configurados**, cobrindo todas as regras de negócio, multicanalidade e validações exigidas no escopo do MVP (incluindo falha por falta de estoque e pagamentos recusados).

### ⚠️ Instruções de Teste (Importante):

Para que os testes funcionem perfeitamente sem erros de concorrência ou status inválido, siga este fluxo:

1. Importe o arquivo `collection_testes.json` no seu Postman ou Insomnia.
2. Certifique-se de que o banco de dados está limpo (recém-criado pelo `seed.py`) e que o servidor local está rodando.
3. Execute as requisições **na ordem em que aparecem nas pastas** (de cima para baixo). 
4. *Nota sobre o estado:* O sistema possui travas de segurança. Se você aprovar o pagamento de um pedido (T09) ou mudar seu status para a cozinha (T10), tentativas subsequentes de pagar o mesmo pedido retornarão Erro 400 (Bad Request). Para testar pagamentos novamente, crie um novo pedido no T08 e atualize a variável `pedidoId` no JSON da requisição.

## 🏗️ Arquitetura em Camadas (Domain-Driven Design simplificado)
O projeto foi estruturado separando as responsabilidades para facilitar a manutenção e escalabilidade:
* `app/api/`: Controladores e Rotas (Endpoints - `routes.py`).
* `app/application/`: Regras de negócio e Serviços (`services.py`).
* `app/domain/`: Contratos de entrada/saída e validações (`schemas.py`).
* `app/infrastructure/`: Conexão com o banco, ORM e Entidades (`models.py`, `database.py`).

#
#### _Desenvolvido para a Disciplina Eletiva IV: Projeto Multidisciplinar de Análise e Desenvolvimento de Sistemas._
