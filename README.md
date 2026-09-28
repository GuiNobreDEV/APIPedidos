# API de Pedidos — Trabalho 1

API REST para cadastro e gerenciamento de pedidos, desenvolvida em Python com FastAPI, SQLAlchemy e PostgreSQL.

## Integrantes

Preencha com os integrantes do grupo antes da criação da tag final:

| Nome completo               | Turma  | RA      |
| --------------------------- | ------ | ------- |
| Guilherme Nobre Evangelista | CC8Q13 | G804619 |
| Lucas Saraiva Carnauba      | CC8Q13 | G7631G9 |
| Kaique Fernandes Leal       | CC8P13 | G797FG7 |

## Tecnologias

- Python 3.12
- FastAPI
- Uvicorn
- SQLAlchemy
- PostgreSQL 16
- Pydantic / pydantic-settings
- Docker
- Docker Compose

## Arquitetura

A aplicação utiliza três camadas lógicas no mesmo container:

```text
Cliente HTTP
    |
    v
API / Router
    |
    v
Service
    |
    v
Repository
    |
    v
SQLAlchemy
    |
    v
PostgreSQL
```

O PostgreSQL executa separadamente em seu próprio container.

## Estrutura

```text
.
├── app/
│   ├── main.py
│   ├── database.py
│   ├── api/
│   │   └── pedidos.py
│   ├── services/
│   │   └── pedido_service.py
│   ├── repositories/
│   │   └── pedido_repository.py
│   ├── models/
│   │   └── pedido.py
│   └── schemas/
│       └── pedido.py
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .env.example
├── .dockerignore
├── .gitignore
└── README.md
```

## Execução

A solução é autocontida e deve ser executada com Docker.

```bash
git clone <URL_DO_REPOSITORIO>
cd <NOME_DO_REPOSITORIO>
git checkout APIPedidos-1-final
docker compose up -d --build
```

O comando `docker compose up -d --build` inicia a API no serviço `pedidos` e o PostgreSQL no serviço `postgres`.

Não é necessário instalar Python, criar banco de dados ou instalar dependências manualmente no host.

## Acesso

- API: http://localhost:8000
- Swagger: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
- Health: http://localhost:8000/health

## Endpoints

### Criar pedido

`POST /pedidos`

Exemplo de entrada:

```json
{
  "cliente": "Lucas",
  "produto": "Notebook",
  "quantidade": 2,
  "valor_unitario": 2500.0
}
```

A aplicação calcula `valor_total` e define o status inicial como `CRIADO`.

### Consultar pedido

`GET /pedidos/{id}`

Retorna `200 OK` quando o pedido existe e `404 Not Found` quando não existe.

### Listar pedidos

`GET /pedidos`

Retorna a coleção de pedidos persistidos.

### Alterar status

`PATCH /pedidos/{id}/status`

Exemplo:

```json
{
  "status": "CONFIRMADO"
}
```

Estados:

- `CRIADO`
- `CONFIRMADO`
- `CANCELADO`

Transições implementadas:

```text
CRIADO -> CONFIRMADO
CRIADO -> CANCELADO
CONFIRMADO -> CANCELADO
```

### Saúde

`GET /health`

Resposta:

```json
{
  "status": "ok"
}
```

## PostgreSQL e persistência

O PostgreSQL é executado como componente independente e utiliza o volume Docker `dados_postgres`.

A aplicação aguarda uma conexão válida com o banco antes de criar as tabelas e iniciar o atendimento da API.

Reiniciar somente o container `pedidos` não remove os pedidos armazenados no PostgreSQL.

## Configuração

A conexão é configurada pela variável de ambiente `DATABASE_URL`. O Docker Compose fornece essa variável automaticamente para o container da aplicação.

## Parar a solução

```bash
docker compose down
```

Para remover também os dados persistidos:

```bash
docker compose down -v
```

## Versão final da entrega

A versão submetida para avaliação deve estar associada à tag:

```text
APIPedidos-1-final
```
