# Instalação e Execução

Esta seção descreve como configurar o ambiente de desenvolvimento e executar o sistema.

## Pré-requisitos

-   **Docker** e **Docker Compose** instalados.
-   **Python 3.12** (opcional, para execução direta do backend).
-   **Node.js 18+** e **npm/yarn** (opcional, para execução direta do frontend).

## 1. Configuração com Docker Compose (Recomendado)

A maneira mais rápida de rodar o projeto completo é usando o Docker Compose.

1.  **Variáveis de Ambiente:**
    Crie os arquivos `.env` nos diretórios `backend/` e `frontend/` baseados nos arquivos de exemplo:
    ```bash
    cp backend/example.env backend/.env
    cp frontend/example.env frontend/.env
    ```

2.  **Construir e Iniciar os Serviços:**
    No diretório raiz do projeto, execute:
    ```bash
    docker compose up --build
    ```

3.  **Acesso:**
    -   **Frontend:** `http://localhost:8080` (conforme configurado no `frontend/Dockerfile` ou no proxy reverso).
    -   **Backend (API):** `http://localhost:8000/api/`
    -   **Admin Django:** `http://localhost:8000/admin/`

## 2. Configuração para Desenvolvimento (Execução Local)

Se você preferir executar os serviços fora do Docker para desenvolvimento rápido:

### Backend

1.  Crie um ambiente virtual:
    ```bash
    cd backend
    python -m venv .venv
    source .venv/bin/activate  # No Windows: .venv\Scripts\activate
    ```
2.  Instale as dependências:
    ```bash
    pip install -r requirements.txt
    ```
3.  Configure o banco de dados PostgreSQL (ou utilize um banco local e atualize o `.env`).
4.  Execute as migrações:
    ```bash
    python manage.py migrate
    ```
5.  Inicie o servidor de desenvolvimento:
    ```bash
    python manage.py runserver
    ```

### Frontend

1.  Instale as dependências:
    ```bash
    cd frontend
    npm install  # ou yarn install
    ```
2.  Inicie o servidor de desenvolvimento:
    ```bash
    npm run serve  # ou yarn serve
    ```

## 3. Comandos Importantes

### Django (Backend)

-   **Criar um superuser:**
    ```bash
    docker compose exec backend python manage.py createsuperuser
    ```
-   **Rodar testes:**
    ```bash
    docker compose exec backend python manage.py test
    ```

### Vue.js (Frontend)

-   **Build para produção:**
    ```bash
    npm run build
    ```
-   **Executar linter:**
    ```bash
    npm run lint
    ```
