# OrientaTCC — API Projetos

Serviço responsável pelo cadastro e consulta de projetos de TCC.

## Endpoints

| Método | Rota | Descrição |
|---|---|---|
| `GET` | `/health` | Verificação de saúde |
| `POST` | `/projects` | Cadastra um projeto |
| `GET` | `/projects` | Lista projetos (`skip` e `limit` opcionais) |
| `GET` | `/projects/{id}` | Consulta um projeto |
| `PATCH` | `/projects/{id}` | Atualiza parcialmente um projeto |
| `DELETE` | `/projects/{id}` | Remove um projeto |

A documentação interativa do FastAPI fica em `/docs`.

## Campos do projeto

`title`, `student_name` e `advisor_name` são obrigatórios. `description` é opcional e `status` começa como `planned` (valores previstos: `planned`, `in_progress`, `completed`).

## Execução local

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Sem `DATABASE_URL`, o serviço usa SQLite em `orienta_tcc.db`. Para PostgreSQL, configure `DATABASE_URL`; o Docker Compose já define essa variável.

## Testes

```bash
pytest -q
```
