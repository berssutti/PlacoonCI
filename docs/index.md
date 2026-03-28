# Visão Geral do Projeto

Bem-vindo à documentação do projeto de **PlacoonCI**.

Este sistema foi desenvolvido para facilitar o gerenciamento, monitoramento e previsão de ressarcimento de custos indiretos em projetos. Ele permite o acompanhamento detalhado de parcelas (installments), áreas de atuação e o status financeiro global de cada iniciativa.

## Arquitetura

O projeto adota uma arquitetura clássica de desacoplamento entre frontend e backend, comunicando-se via uma API REST.

### Componentes Principais

1.  **Backend (API REST):**
    *   Construído com **Django 5** e **Django REST Framework**.
    *   Responsável pela lógica de negócio, persistência de dados e autenticação.
    *   Utiliza sinais (signals) do Django para manter totais financeiros sincronizados automaticamente conforme parcelas são atualizadas.
2.  **Frontend (SPA):**
    *   Desenvolvido com **Vue.js 3** e **Vuetify 3**.
    *   Interface reativa e moderna para visualização de dados e gerenciamento de projetos.
    *   Consome a API de forma assíncrona.
3.  **Banco de Dados:**
    *   **PostgreSQL** é utilizado para armazenamento robusto e relacional.
4.  **Containerização:**
    *   **Docker** e **Docker Compose** são utilizados para orquestrar os serviços e garantir paridade entre os ambientes de desenvolvimento e produção.

## Tecnologias

- **Backend:** Python, Django, Django Rest Framework, Django Filter, Python Decouple.
- **Frontend:** JavaScript, Vue 3, Vuetify 3, Axios, Chart.js.
- **Banco de dados:** PostgreSQL.
- **Infraestrutura:** Docker, Nginx (em produção).

## Estrutura do Repositório

O repositório está organizado da seguinte forma:

- `backend/`: Código fonte da API Django, modelos, serializers e comandos de gerenciamento.
- `frontend/`: Aplicação Vue.js, componentes, roteamento e estilos.
- `docs/`: Arquivos de documentação em Markdown (MkDocs).
- `docker-compose.yml`: Definição dos serviços para execução local.
