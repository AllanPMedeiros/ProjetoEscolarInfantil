# 🏫 Sistema de Gestão Escolar Infantil

## 📋 O que é?
O Sistema de Gestão Escolar Infantil é uma aplicação web desenvolvida para auxiliar na administração de escolas infantis, oferecendo uma plataforma centralizada para gerenciar todos os aspectos operacionais da instituição.

## ⚙️ O que faz?
O sistema permite:
- Gerenciamento completo de alunos (cadastro, consulta, atualização e exclusão)
- Controle de professores e suas atribuições
- Organização de turmas e atividades pedagógicas
- Registro e acompanhamento de presenças dos alunos
- Controle de pagamentos e mensalidades
- Geração de relatórios e métricas de desempenho
- Monitoramento da saúde do sistema através de ferramentas de observabilidade

## 🛠️ Tecnologias Utilizadas
- 🐍 **Backend**: Python com Flask (API RESTful)
- 🐘 **Banco de Dados**: PostgreSQL
- 🐳 **Containerização**: Docker e Docker Compose
- 📚 **Documentação API**: Flasgger/Swagger
- 📊 **Observabilidade**:
  - 📡 Prometheus para coleta de métricas
  - 📈 Grafana para visualização de dashboards
  - 🔄 Postgres-exporter para exportação de métricas do banco de dados

## 📖 Documentação Adicional
- [📚 Documentação da API](ProjetoEscolar/App/README.md) - Detalhes sobre endpoints e uso da API
- [🗄️ Documentação do Banco de Dados](ProjetoEscolar/Documentos/documentação.md) - Informações sobre estrutura do banco e configuração do BD para rodar no docker
- [🧪 Documentação dos Testes](ProjetoEscolar/testes/README.md) - Guia para execução e criação de testes

## 📁 Estrutura do Projeto
```
ProjetoEscolar/
├── App/                    # Código fonte da aplicação
│   ├── Utils/              # Utilitários e configurações
│   │   ├── __init__.py     # Arquivo init para tornar a pasta um pacote Python
│   │   ├── bd.py           # Conexão com banco de dados
│   │   └── paramsBD.yml    # Parâmetros de conexão
│   ├── __init__.py         # Factory da aplicação Flask + Swagger
│   ├── crudAlunos.py       # CRUD de alunos
│   ├── crudAtividade_Aluno.py # Relação entre atividades e alunos
│   ├── crudAtividades.py   # CRUD de atividades
│   ├── crudPagamentos.py   # CRUD de pagamentos
│   ├── crudPresencas.py    # CRUD de presenças
│   ├── crudProfessores.py  # CRUD de professores
│   ├── crudTurmas.py       # CRUD de turmas
│   ├── crudUsuarios.py     # CRUD de usuários
│   ├── README.md           # Documentação da API
│   └── requirements.txt    # Dependências Python
├── db/                     # Configuração do banco de dados
│   ├── Dockerfile          # Dockerfile para o PostgreSQL
│   └── escola.sql          # Script de inicialização do banco
├── Documentos/             # Documentação do projeto
│   ├── documentação.md     # Documentação do banco
│   └── Mer do Sistema de Gestão Escolar Infantil.pdf
├── Observabilidade/        # Configurações para monitoramento
│   ├── grafana/            # Configuração do Grafana
│   ├── postgres-exporter/  # Exportador de métricas do PostgreSQL
│   └── prometheus/         # Configuração do Prometheus
├── scripts/                # Pasta scripts contendo o arquivo DDL comentado
├── testes/                 # Pasta contendo os testes unitários dos CRUDS
├──.gitignore               # Arquivos para não serem versionados
├── app.py                  # Ponto de entrada da aplicação
├── compose.yml             # Configuração do Docker Compose
└── dockerfile.app          # Dockerfile para a aplicação
```

## 🚀 Passo a Passo para Configurar e Rodar o Ambiente Docker

### 1. 📥 Clonar o Repositório
```bash
git clone https://github.com/seu-usuario/ProjetoEscolarInfantil.git
cd ProjetoEscolarInfantil
```

### 2. 📂 Navegar para a Pasta do Projeto
```bash
cd ProjetoEscolar
```

### 3. 🐳 Iniciar os Containers
Execute o seguinte comando para construir e iniciar todos os serviços:
```bash
docker-compose up -d
```

Este comando irá:
- Construir as imagens Docker necessárias
- Criar e iniciar os containers para:
  - Banco de dados PostgreSQL (porta 3001)
  - API backend em Flask (porta 5000)
  - Prometheus para coleta de métricas (porta 9090)
  - Grafana para visualização de métricas (porta 3000)
  - Postgres-exporter para exportar métricas do PostgreSQL (porta 9187)

### 4. 🔍 Verificar o Status dos Containers
```bash
docker-compose ps
```

Todos os serviços devem estar com o status "Up".

### 5. 🌐 Acessar a API Backend
A API estará disponível em:
```
http://localhost:5000
```

A documentação da API (Swagger/Flasgger) pode ser acessada em:
```
http://localhost:5000/docs/
```

### 6. 💾 Acessar o Banco de Dados
Para conectar ao PostgreSQL usando ferramentas como DBeaver, pgAdmin ou outras ferramentas de gerenciamento de banco de dados, utilize as seguintes configurações:
```
Host: localhost
Porta: 3001
Banco de dados: escola
Usuário: admin
Senha: admin123
```

### 7. 📊 Acessar as Ferramentas de Observabilidade
- **Grafana**: http://localhost:3000
  - Usuário: admin
  - Senha: admin
- **Prometheus**: http://localhost:9090

#### 📈 Configurando o Grafana para monitorar o PostgreSQL:

1. Acesse o Grafana em http://localhost:3000 e faça login com as credenciais acima
2. Vá para "Configuration" > "Data Sources" (ícone de engrenagem no menu lateral)
3. Clique em "Add data source"
4. Selecione "Prometheus" como tipo de fonte de dados
5. Configure a URL como `http://prometheus:9090`
6. Clique em "Save & Test" para verificar a conexão

7. Para criar um dashboard para o PostgreSQL Exporter:
   - Vá para "Create" > "Import" no menu lateral
   - Insira o ID 9628 ( PostgreSQL Exporter Overview).
   - Na tela de importação, selecione o Prometheus como fonte de dados
   - Clique em "Import"

8. O dashboard agora mostrará métricas como:
   - Conexões ativas
   - Transações por segundo
   - Uso de CPU e memória
   - Operações de leitura/escrita
   - Tempo de resposta de consultas

### 8. 🛑 Parar os Containers
Para parar todos os containers sem removê-los:
```bash
docker compose stop
```

Para parar e remover todos os containers:
```bash
docker compose down
```

Para parar, remover todos os containers e apagar os volumes (isso apagará os dados do banco):
```bash
docker compose down -v
```