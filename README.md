## Execução Orçamentaria

Este documento detalha as especificações para colocar o "Sistema de Execução Orçamentária" em um ambiente de produção, cobrindo aspectos técnicos, arquitetônicos e operacionais.

### 1. Visão Geral do Projeto

O sistema é uma aplicação projetada para gerenciar e monitorar e prever o ressacimento de custos indiretos.

### 2. Pilha Tecnológica

Principais tecnologias do projeto:

* **Frontend:**
    * Vue.js 3
    * Vuetify 3
* **Backend:**
    * Django 5
    * Django REST Framework
    * PostgreSQL
* **Infraestrutura e Conteinerização:**
    * Docker
    * Docker Compose

### 3. Arquitetura de Implantação (Conceitual)

A arquitetura de implantação em produção será baseada em contêineres Docker(para ambientes de produção não é recomendado docker compose). Os principais componentes incluirão:

* **Contêiner Frontend:** Servindo a aplicação Vue.js.
* **Contêiner Backend:** Executando a aplicação Django/Django REST Framework.
* **Contêiner Banco de Dados:** Instância PostgreSQL dedicada.
* **Servidor Web/Proxy Reverso:** Recomenda-se o uso de um servidor web como Nginx ou Caddy para atuar como proxy reverso, balanceador de carga e para servir arquivos estáticos, bem como para gerenciar certificados SSL.

### 4. Pré-requisitos para Produção

Para a implantação em produção, o ambiente deve atender aos seguintes pré-requisitos:

* **Servidor:** Um servidor (físico ou virtual) com capacidade de CPU, memória e armazenamento adequadas para a carga esperada.
* **Sistema Operacional:** Um sistema operacional compatível com Docker (ex: Ubuntu Server, Debian, CentOS, RHEL).
* **Docker e Docker Compose:** Ambos devem estar instalados e configurados no servidor de produção.
* **Acesso à Internet:** Para download de imagens Docker e dependências.
* **Domínio/Subdomínio:** Um domínio ou subdomínio configurado e apontando para o endereço IP do servidor de produção.
* **Certificado SSL:** Para garantir a comunicação segura (HTTPS).

### 5. Etapas de Implantação (Geral)

As etapas gerais para implantar o sistema em produção são as seguintes:

1.  **Preparação do Servidor:**
    * Atualizar o sistema operacional.
    * Instalar Docker e Docker Compose.
    * Configurar o firewall para permitir o tráfego nas portas necessárias (ex: 80, 443).
2.  **Obtenção do Código Fonte:**
    * Clonar o repositório Git (`https://github.com/berssutti/execucao-orcamentaria`) para o servidor de produção.
3.  **Configuração de Variáveis de Ambiente:**
    * Criar um arquivo `.env` (ou similar) para definir variáveis de ambiente específicas de produção, como credenciais do banco de dados, chaves secretas do Django, URLs da API, etc. (Detalhes específicos devem ser obtidos da documentação do projeto, se disponível, ou definidos conforme as necessidades de segurança e configuração).
4.  **Construção das Imagens Docker:**
    * Navegar até o diretório raiz do projeto.
    * Executar o comando `docker compose build` para construir as imagens dos contêineres a partir dos Dockerfiles.
5.  **Inicialização dos Contêineres:**
    * Executar o comando `docker compose up -d` para iniciar os serviços em segundo plano.
    * Carregar dados iniciais (se houver).
6.  **Configuração do Servidor Web/Proxy Reverso:**
    * Configurar o Nginx/Caddy para direcionar o tráfego para os contêineres apropriados (frontend e backend).
    * Configurar SSL/TLS usando um certificado (ex: Let's Encrypt).

### 6. Variáveis de Ambiente e Configuração

* `DATABASE_URL` (ou variáveis separadas para host, porta, usuário, senha, nome do banco de dados PostgreSQL)
* `SECRET_KEY` (para Django, uma chave secreta forte e única)
* `DEBUG=False` (muito importante para desativar o modo de depuração em produção)
* `ALLOWED_HOSTS` (lista de hosts permitidos para a aplicação Django)
* `CORS_ALLOWED_ORIGINS` (se aplicável para o frontend)
* Variáveis para integração com serviços externos (ex: APIs de terceiros).
