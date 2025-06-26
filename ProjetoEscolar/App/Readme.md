# API Sistema Escola Infantil

## 🏗️ Arquitetura do Backend

### Estrutura do Projeto
```
App/
├── Utils/
│   ├── __init__.py        # # Arquivo __init__.py para tornar a pasta Util um pacote Python. 
│   ├── bd.py              # Conexão com banco de dados
│   └── paramsBD.yml       # Parâmetros de configuração do BD
├── __init__.py            # Factory da aplicação Flask + Swagger
├── crudAlunos.py          # CRUD para gerenciamento de alunos
├── crudAtividade_Aluno.py # CRUD para associação atividade-aluno
├── crudAtividades.py      # CRUD para gerenciamento de atividades
├── crudPagamentos.py      # CRUD para gerenciamento de pagamentos
├── crudPresencas.py       # CRUD para controle de presenças
├── crudProfessores.py     # CRUD para gerenciamento de professores
├── crudTurmas.py          # CRUD para gerenciamento de turmas
├── crudUsuarios.py        # CRUD para gerenciamento de usuários
├── README.md              # Documentação do projeto
└── requirements.txt       # Dependências Python
```

### Tecnologias Utilizadas
- **Framework**: Flask (Python 3.9)
- **Banco de Dados**: PostgreSQL
- **Documentação**: Swagger/Flasgger
- **Containerização**: Docker + Docker Compose
- **Monitoramento**: Prometheus + Grafana

### Padrão Arquitetural
- **Blueprint Pattern**: Cada módulo CRUD é um Blueprint Flask independente
- **Factory Pattern**: Aplicação criada através da função `create_app()`
- **Separação de Responsabilidades**: Utils para conexão BD, CRUDs para lógica de negócio

## 🐳 Executando com Docker

### Pré-requisitos
- Docker
- Docker Compose

### Instruções de Execução

1. **Clone o repositório e navegue até a pasta do projeto:**
```bash
cd ProjetoEscolar
```

2. **Execute o ambiente completo:**
```bash
docker-compose up -d
```

3. **Verificar se os containers estão rodando:**
```bash
docker-compose ps
```

### Serviços Disponíveis
- **API Flask**: http://localhost:5000
- **PostgreSQL**: localhost:3001
- **Swagger UI**: http://localhost:5000/docs/
- **Prometheus**: http://localhost:9090
- **Grafana**: http://localhost:3000

### Comandos Úteis
```bash
# Parar todos os serviços
docker-compose stop

# Rebuild da aplicação
docker-compose up --build api

# Ver logs da API
docker-compose logs -f api

# Acessar container da API
docker-compose exec api bash
```

## 📚 Endpoints da API CRUD

### 👨‍🎓 Alunos (`/alunos`)
```http
POST   /alunos           # Criar aluno
GET    /alunos           # Listar todos os alunos
GET    /alunos/{id}      # Buscar aluno por ID
PUT    /alunos/{id}      # Atualizar aluno
DELETE /alunos/{id}      # Deletar aluno
```

**Exemplo de Payload (POST/PUT):**
```json
{
  "nome_completo": "João Silva",
  "data_nascimento": "2018-05-15",
  "id_turma": 1,
  "nome_responsavel": "Maria Silva",
  "telefone_responsavel": "(11) 99999-9999",
  "email_responsavel": "maria@email.com",
  "informacoes_adicionais": "Alergia a amendoim"
}
```

### 👩‍🏫 Professores (`/professores`)
```http
POST   /professores      # Criar professor
GET    /professores      # Listar todos os professores
GET    /professores/{id} # Buscar professor por ID
PUT    /professores/{id} # Atualizar professor
DELETE /professores/{id} # Deletar professor
```

**Exemplo de Payload (POST/PUT):**
```json
{
  "nome_completo": "Ana Silva Santos",
  "email": "ana.santos@escola.com",
  "telefone": "(11) 98765-4321"
}
```

### 🏫 Turmas (`/turmas`)
```http
POST   /turmas           # Criar turma
GET    /turmas           # Listar todas as turmas
GET    /turmas/{id}      # Buscar turma por ID
PUT    /turmas/{id}      # Atualizar turma
DELETE /turmas/{id}      # Deletar turma
```

**Exemplo de Payload (POST/PUT):**
```json
{
  "nome_turma": "Jardim I - Manhã",
  "id_professor": 1,
  "horario": "08:00 - 12:00"
}
```

### 📝 Atividades (`/atividades`)
```http
POST   /atividades       # Criar atividade
GET    /atividades       # Listar todas as atividades
GET    /atividades/{id}  # Buscar atividade por ID
PUT    /atividades/{id}  # Atualizar atividade
DELETE /atividades/{id}  # Deletar atividade
```

**Exemplo de Payload (POST/PUT):**
```json
{
  "descricao": "Pintura com tinta guache - Tema: Natureza",
  "data_realizacao": "2024-03-15"
}
```

### 📊 Atividade-Aluno (`/atividades_alunos`)
```http
POST   /atividades_alunos                    # Associar aluno à atividade
GET    /atividades_alunos                    # Listar associações
GET    /atividades_alunos/{id_ativ}/{id_aluno} # Buscar associação específica
DELETE /atividades_alunos/{id_ativ}/{id_aluno} # Remover associação
```

**Exemplo de Payload (POST):**
```json
{
  "id_atividade": 1,
  "id_aluno": 5
}
```

### 📅 Presenças (`/presencas`)
```http
POST   /presencas        # Registrar presença
GET    /presencas        # Listar presenças
GET    /presencas/{id}   # Buscar presença por ID
PUT    /presencas/{id}   # Atualizar presença
DELETE /presencas/{id}   # Deletar presença
```

**Exemplo de Payload (POST/PUT):**
```json
{
  "id_aluno": 3,
  "data_presenca": "2024-03-15",
  "presente": true
}
```

**Parâmetros de Consulta (GET /presencas):**
- `id_aluno`: Filtrar por aluno específico
- `data_inicio`: Data inicial para filtro
- `data_fim`: Data final para filtro
- `presente`: Filtrar por status (true/false)

**Exemplo de Payload (POST/PUT):**
```json
{
  "id_aluno": 3,
  "data_presenca": "2024-03-15",
  "presente": true
}
```

**Parâmetros de Consulta (GET /presencas):**
- `id_aluno`: Filtrar por aluno específico
- `data_inicio`: Data inicial para filtro
- `data_fim`: Data final para filtro
- `presente`: Filtrar por status (true/false)

### 💰 Pagamentos (`/pagamentos`)
```http
POST   /pagamentos       # Criar pagamento
GET    /pagamentos       # Listar pagamentos
GET    /pagamentos/{id}  # Buscar pagamento por ID
PUT    /pagamentos/{id}  # Atualizar pagamento
DELETE /pagamentos/{id}  # Deletar pagamento
```

**Exemplo de Payload (POST/PUT):**
```json
{
  "id_aluno": 2,
  "data_pagamento": "2024-03-01",
  "valor_pago": 450.00,
  "forma_pagamento": "PIX",
  "referencia": "Mensalidade Março/2024",
  "status": "Pago"
}
```

### 👤 Usuários (`/usuarios`)
```http
POST   /usuarios         # Criar usuário
GET    /usuarios         # Listar usuários
GET    /usuarios/{id}    # Buscar usuário por ID
PUT    /usuarios/{id}    # Atualizar usuário
DELETE /usuarios/{id}    # Deletar usuário
```

**Exemplo de Payload (POST/PUT):**
```json
{
  "login": "ana.santos",
  "senha": "MinhaSenh@123",
  "nivel_acesso": "professor",
  "id_professor": 1
}
```

**Observações sobre Usuários:**
- Senha deve ter pelo menos 8 caracteres com letras e números
- Login deve ser único no sistema
- Níveis de acesso: "admin", "professor", "usuario"

## 📖 Documentação Swagger

### Acessando a Documentação
A documentação interativa da API está disponível através do Swagger UI:

**URL**: http://localhost:5000/docs/

### Funcionalidades do Swagger
- **Explorar Endpoints**: Visualize todos os endpoints disponíveis organizados por tags
- **Testar API**: Execute requisições diretamente pela interface
- **Visualizar Schemas**: Veja a estrutura dos dados de entrada e saída
- **Exemplos**: Acesse exemplos de payloads para cada endpoint

### Estrutura da Documentação
- **Tags**: Endpoints organizados por entidade (Alunos, Professores, etc.)
- **Parâmetros**: Descrição detalhada de cada parâmetro
- **Responses**: Códigos de status e estruturas de resposta
- **Schemas**: Modelos de dados com validações

### Testando via Swagger
1. Acesse http://localhost:5000/docs/
2. Selecione o endpoint desejado
3. Clique em "Try it out"
4. Preencha os parâmetros necessários
5. Execute a requisição
6. Visualize a resposta

## 🔧 Configuração do Banco de Dados

### Parâmetros de Conexão
Os parâmetros de conexão estão configurados em `Utils/paramsBD.yml`:
```yaml
db_host: db
db_port: 5432
db_name: escola
db_user: admin
db_password: admin123
```

### Variáveis de Ambiente (Docker)
```env
DB_HOST=db
DB_PORT=5432
DB_NAME=escola
DB_USER=admin
DB_PASSWORD=admin123
```

## 🚀 Desenvolvimento

### Instalação Local (sem Docker)
```bash
# Instalar dependências
pip install -r requirements.txt

# Configurar variáveis de ambiente
export FLASK_ENV=development
export FLASK_APP=app.py

# Executar aplicação
python app.py
```

### Estrutura de Resposta Padrão
```json
{
  "message": "Operação realizada com sucesso",
  "data": { /* dados retornados */ }
}
```

### Tratamento de Erros
```json
{
  "error": "Descrição do erro",
  "status_code": 400
}
```

## 📊 Monitoramento

- **Prometheus**: Coleta de métricas em http://localhost:9090
- **Grafana**: Dashboards em http://localhost:3000 (admin/admin)
- **PostgreSQL Exporter**: Métricas do banco em http://localhost:9187
---

**Desenvolvido para Sistema de Gestão Escolar Infantil**