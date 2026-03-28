# Backend

O backend é construído com Django e Django Rest Framework.

## Estrutura de Diretórios

- `orcamento_execucao`: Contém as configurações do projeto Django.
- `projects`: Contém a aplicação Django para o gerenciamento de projetos.

## Populando o Banco para Testes

O projeto inclui ferramentas para popular o banco de dados com dados iniciais e fictícios para fins de teste.

### Dados Iniciais (Fixtures)

As áreas de conhecimento (`Area`) são carregadas automaticamente durante a primeira migração através de um sinal de `post_migrate` que consome o arquivo `backend/projects/fixtures/init_areas.json`.

### Dados de Teste (Mock Data)

Para gerar dados aleatórios de projetos e parcelas, utilize o comando customizado:

```bash
# Se estiver usando Docker:
docker compose exec backend python manage.py projects_mock_data

# Se estiver localmente:
cd backend
python manage.py projects_mock_data
```

**Opções do Comando:**

- `--projects [N]`: Número de projetos a serem criados (padrão: 100).
- `--installments_per_project [N]`: Média de parcelas por projeto (padrão: 5).
- `--project_areas_per_project [N]`: Média de áreas por projeto (padrão: 2).
- `--clear-data`: Limpa todos os projetos e parcelas existentes antes de gerar novos dados.

Exemplo de uso:
```bash
python manage.py projects_mock_data --projects 10 --clear-data
```

---
Este comando utiliza a biblioteca **Faker** para gerar nomes, descrições e datas realistas, e recalcula automaticamente os totais financeiros de cada projeto após a inserção.
