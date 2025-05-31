# Documentação do Projeto de Execução Orçamentária

## Visão Geral
Este projeto é um sistema de execução orçamentária desenvolvido, utilizando Docker para containerização. O sistema é composto por três componentes principais: um frontend em Vue.js, um backend em Django e um banco de dados PostgreSQL.

## Especificações Técnicas

### Backend
- **Framework**: Django 5.1.4
- **API**: Django REST Framework
- **Banco de Dados**: PostgreSQL 15
- **Porta**: 8000

### Frontend
- **Framework**: Vue.js 3
- **UI Framework**: Vuetify 3
- **Gráficos**: Chart.js
- **Porta**: 8080

### Banco de Dados
- **Sistema**: PostgreSQL 15
- **Porta**: 5432
- **Credenciais**:
  - Database: orcamento-execucao_db
  - Usuário: admin
  - Senha: admin

## Requisitos do Sistema
- Docker
- Docker Compose
- Git

## Instalação e Execução

### 1. Clone o Repositório
```bash
git clone [URL_DO_REPOSITÓRIO]
cd execucao-orcamentaria
```
### 2. Variáveis de Ambiente
Crie dois arquivos `.env`, seguindo os exemplos dos arquivo `example.env`. Deve ser criado um arquivo `.env` no diretório `frontend/` e outro no diretório `backend/`. 

### 3. Inicialização com Docker
Para iniciar o projeto, execute o seguinte comando na raiz do projeto:
```bash
docker-compose up --build
```

Este comando irá:
- Construir as imagens Docker necessárias
- Iniciar o banco de dados PostgreSQL
- Iniciar o servidor backend Django
- Iniciar o servidor frontend Vue.js

### 3. Acessando a Aplicação
Após a inicialização, você pode acessar:
- Frontend: http://localhost:8080
- Backend API: http://localhost:8000
- Banco de Dados: localhost:5432

## Desenvolvimento

### Modo de Desenvolvimento
O projeto está configurado com hot-reload para desenvolvimento:
- Alterações no backend serão automaticamente detectadas e o servidor será reiniciado
- Alterações no frontend serão automaticamente compiladas e o navegador será atualizado
  
### Popular Banco de dados

Com os serviços rodando: O comando abaixo vai limpar todos os dados do banco e em seguida popular o banco de dados com 20 projetos.

```python
docker compose exec backend python3 manage.py projects_mock_data --projects 20 --clear-data
```
O comando tem um *helper* que oferece mais informações.
```python
docker compose exec backend python3 manage.py projects_mock_data --help
```

### Estrutura de Diretórios
```
execucao-orcamentaria/
├── backend/           # Aplicação Django
├── frontend/          # Aplicação Vue.js
├── docs/             # Documentação
└── docker-compose.yml # Configuração Docker
```

## Troubleshooting

### Problemas Comuns
1. **Portas em Uso**
   - Verifique se as portas 8080, 8000 e 5432 estão disponíveis
   - Se necessário, altere as portas no docker-compose.yml

2. **Erros de Build**
   - Execute `docker-compose down` para remover containers antigos
   - Execute `docker-compose build --no-cache` para forçar rebuild

3. **Problemas de Banco de Dados**
   - Verifique se o volume do PostgreSQL foi criado corretamente
   - Execute `docker-compose down -v` para remover volumes e recriar o banco

## Contribuição
Para contribuir com o projeto:
1. Crie uma branch para sua feature
2. Faça suas alterações
3. Envie um Pull Request

## Suporte
Em caso de problemas ou dúvidas, abra uma issue no repositório do projeto. 
