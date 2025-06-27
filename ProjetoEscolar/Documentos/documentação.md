# 📊 Documentação do Banco de Dados - Sistema de Gestão Escolar Infantil

## 🎯 Visão Geral

O banco de dados foi projetado para atender às necessidades específicas de uma escola infantil, seguindo princípios de normalização e integridade referencial. O modelo relacional escolhido oferece flexibilidade para expansões futuras e garante a consistência dos dados.

## 🏗️ Arquitetura do Modelo de Dados

### Características Principais:
- **SGBD**: PostgreSQL 
- **Normalização**: 3ª Forma Normal (3FN)
- **Integridade Referencial**: Chaves estrangeiras com constraints
- **Escalabilidade**: Estrutura preparada para crescimento
- **Segurança**: Senhas criptografadas e controle de acesso

## 📋 Estrutura das Tabelas

### 1. 👨‍🏫 Tabela `professor`
**Propósito**: Gerenciar informações dos docentes da instituição.

| Campo | Tipo | Restrições | Descrição |
|-------|------|------------|-----------|
| `id_professor` | SERIAL | PRIMARY KEY | Identificador único autoincremental |
| `nome_completo` | VARCHAR(255) | NOT NULL | Nome completo do professor |
| `email` | VARCHAR(100) | - | Email para contato e notificações |
| `telefone` | VARCHAR(20) | - | Telefone para contato |

**Relacionamentos**: 1:N com `turma` e `usuario`

### 2. 🏫 Tabela `turma`
**Propósito**: Organizar alunos em grupos de aprendizagem com professor responsável.

| Campo | Tipo | Restrições | Descrição |
|-------|------|------------|-----------|
| `id_turma` | SERIAL | PRIMARY KEY | Identificador único da turma |
| `nome_turma` | VARCHAR(50) | NOT NULL | Nome/código da turma (ex: "Maternal A") |
| `id_professor` | INT | FOREIGN KEY | Referência ao professor responsável |
| `horario` | VARCHAR(100) | - | Descrição do horário de funcionamento |

**Relacionamentos**: N:1 com `professor`, 1:N com `aluno`

### 3. 👶 Tabela `aluno`
**Propósito**: Centralizar informações dos estudantes e seus responsáveis.

| Campo | Tipo | Restrições | Descrição |
|-------|------|------------|-----------|
| `id_aluno` | SERIAL | PRIMARY KEY | Identificador único do aluno |
| `nome_completo` | VARCHAR(255) | NOT NULL | Nome completo do aluno |
| `data_nascimento` | DATE | NOT NULL | Data de nascimento para controle etário |
| `id_turma` | INT | FOREIGN KEY | Turma em que está matriculado |
| `nome_responsavel` | VARCHAR(255) | - | Nome do responsável legal |
| `telefone_responsavel` | VARCHAR(20) | - | Contato telefônico do responsável |
| `email_responsavel` | VARCHAR(100) | - | Email do responsável |
| `informacoes_adicionais` | TEXT | - | Observações especiais (alergias, etc.) |

**Relacionamentos**: N:1 com `turma`, 1:N com `pagamento`, `presenca` e `atividade_aluno`

### 4. 💰 Tabela `pagamento`
**Propósito**: Controlar transações financeiras e mensalidades.

| Campo | Tipo | Restrições | Descrição |
|-------|------|------------|-----------|
| `id_pagamento` | SERIAL | PRIMARY KEY | Identificador único do pagamento |
| `id_aluno` | INT | FOREIGN KEY | Aluno relacionado ao pagamento |
| `data_pagamento` | DATE | NOT NULL | Data da transação |
| `valor_pago` | DECIMAL(10,2) | NOT NULL | Valor monetário com precisão |
| `forma_pagamento` | VARCHAR(50) | - | Método utilizado (PIX, cartão, etc.) |
| `referencia` | VARCHAR(100) | - | Código de referência bancária |
| `status` | VARCHAR(20) | - | Situação (Pago, Pendente, Cancelado) |

**Relacionamentos**: N:1 com `aluno`

### 5. 📅 Tabela `presenca`
**Propósito**: Monitorar frequência escolar dos alunos.

| Campo | Tipo | Restrições | Descrição |
|-------|------|------------|-----------|
| `id_presenca` | SERIAL | PRIMARY KEY | Identificador único do registro |
| `id_aluno` | INT | FOREIGN KEY | Aluno avaliado |
| `data_presenca` | DATE | NOT NULL | Data da verificação |
| `presente` | BOOLEAN | - | Indicador de presença (true/false) |

**Relacionamentos**: N:1 com `aluno`

### 6. 📚 Tabela `atividade`
**Propósito**: Catalogar atividades pedagógicas realizadas.

| Campo | Tipo | Restrições | Descrição |
|-------|------|------------|-----------|
| `id_atividade` | SERIAL | PRIMARY KEY | Identificador único da atividade |
| `descricao` | TEXT | NOT NULL | Detalhamento da atividade |
| `data_realizacao` | DATE | NOT NULL | Data de execução |

**Relacionamentos**: N:N com `aluno` (via `atividade_aluno`)

### 7. 🎯 Tabela `atividade_aluno`
**Propósito**: Relacionar alunos às atividades com avaliação de desempenho.

| Campo | Tipo | Restrições | Descrição |
|-------|------|------------|-----------|
| `id_atividade` | INT | PRIMARY KEY, FOREIGN KEY | Referência à atividade |
| `id_aluno` | INT | PRIMARY KEY, FOREIGN KEY | Referência ao aluno |
| `desempenho` | VARCHAR(50) | - | Avaliação qualitativa |
| `observacoes` | TEXT | - | Comentários adicionais |

**Chave Primária Composta**: (`id_atividade`, `id_aluno`)
**Relacionamentos**: N:1 com `atividade` e `aluno`

### 8. 👤 Tabela `usuario`
**Propósito**: Controlar acesso ao sistema com diferentes níveis de permissão.

| Campo | Tipo | Restrições | Descrição |
|-------|------|------------|-----------|
| `id_usuario` | SERIAL | PRIMARY KEY | Identificador único do usuário |
| `login` | VARCHAR(50) | UNIQUE, NOT NULL | Nome de usuário único |
| `senha` | VARCHAR(255) | NOT NULL | Hash da senha (bcrypt) |
| `nivel_acesso` | VARCHAR(20) | - | Tipo de permissão (admin, professor) |
| `id_professor` | INT | FOREIGN KEY | Vinculação opcional com professor |

**Relacionamentos**: N:1 com `professor`

## 🐳 Configuração do Banco no Docker

### Dockerfile do PostgreSQL
```dockerfile
FROM postgres:latest

ENV POSTGRES_DB=escola
ENV POSTGRES_USER=admin
ENV POSTGRES_PASSWORD=admin123

COPY escola.sql /docker-entrypoint-initdb.d/

EXPOSE 5432
```

### Docker Compose - Serviço de Banco
```yaml
services:
  db:
    build: ./db
    container_name: escola_db
    environment:
      POSTGRES_DB: escola
      POSTGRES_USER: admin
      POSTGRES_PASSWORD: admin123
    volumes:
      - db_data:/var/lib/postgresql/data
    networks:
      - app_network
    ports:
      - "3001:5432"
```

### Características da Configuração:
- **Imagem Base**: PostgreSQL oficial (latest)
- **Inicialização Automática**: Script SQL executado na criação
- **Persistência**: Volume Docker para dados
- **Rede Isolada**: Comunicação segura entre containers
- **Porta Externa**: 3001 para acesso externo

## 🔗 Relacionamentos e Integridade

### Diagrama de Relacionamentos:
```
professor (1) ──── (N) turma (1) ──── (N) aluno
    │                                    │
    │                                    ├── (1:N) ──── pagamento
    │                                    ├── (1:N) ──── presenca
    │                                    └── (N:N) ──── atividade
    │                                         │
    └── (1:N) ──── usuario                   └── atividade_aluno
```

### Regras de Integridade:
1. **Cascata**: Exclusão de professor não afeta turmas existentes
2. **Restrição**: Aluno deve estar vinculado a uma turma válida
3. **Unicidade**: Login de usuário deve ser único no sistema
4. **Validação**: Datas não podem ser nulas em registros críticos

## 📊 Dados de Exemplo

O banco é inicializado com dados de exemplo incluindo:
- **4 Professores** com diferentes especialidades
- **4 Turmas** (Maternal, Jardim I, Jardim II, Pré-escola)
- **8 Alunos** distribuídos nas turmas
- **Registros de Pagamento** com diferentes formas
- **Controle de Presença** para acompanhamento
- **Atividades Pedagógicas** com avaliações
- **Usuários do Sistema** com níveis de acesso

## 🚀 Vantagens do Modelo Escolhido

1. **Flexibilidade**: Fácil adição de novos campos e tabelas
2. **Escalabilidade**: Suporta crescimento da instituição
3. **Integridade**: Constraints garantem consistência
4. **Performance**: Índices automáticos em chaves primárias
5. **Manutenibilidade**: Estrutura clara e documentada
6. **Segurança**: Senhas criptografadas e controle de acesso
---

Esta estrutura garante um sistema robusto e escalável para o gerenciamento completo de uma escola infantil, mantendo a integridade dos dados e facilitando futuras expansões.