# Execução Orçamentária

Sistema para gerenciar, monitorar e prever o ressarcimento de custos indiretos em projetos.

## 🚀 Início Rápido

Para rodar o projeto rapidamente usando Docker:

1.  **Configurar ambiente:**
    ```bash
    cp backend/example.env backend/.env
    cp frontend/example.env frontend/.env
    ```

2.  **Iniciar serviços:**
    ```bash
    docker compose up --build
    ```

3.  **Popular dados de teste:**
    ```bash
    docker compose exec backend python manage.py projects_mock_data --projects 20 --clear-data
    ```

4.  **Acessar:**
    -   Frontend: `http://localhost:8080`
    -   API: `http://localhost:8000/api/`

## 📖 Documentação Completa

Para mais detalhes sobre a arquitetura, instalação detalhada e guias do desenvolvedor, consulte a nossa documentação completa em `/docs` ou execute o MkDocs localmente:

```bash
pip install mkdocs-material
mkdocs serve
```

---

## Pilha Tecnológica

*   **Frontend:** Vue.js 3, Vuetify 3
*   **Backend:** Django 5, Django REST Framework
*   **Banco de Dados:** PostgreSQL
*   **Infraestrutura:** Docker, Docker Compose
