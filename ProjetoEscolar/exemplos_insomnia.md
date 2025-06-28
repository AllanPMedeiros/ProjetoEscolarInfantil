# Exemplos de Requisições para o Insomnia

Este arquivo contém exemplos de requisições HTTP (POST, PUT, GET, DELETE e GET com ID) para os CRUDs do sistema escolar infantil. Você pode copiar estes exemplos e usá-los no Insomnia.

## Base URL
 
Url base para ser inserida antes do endpoint (ex no insomnia:localhost:5000/alunos )

```
http://localhost:5000
```

## Alunos

### POST - Criar Aluno

**Endpoint:** `/alunos`

**Método:** `POST`

**Body (JSON):**
```json
{
  "nome_completo": "Maria Silva",
  "data_nascimento": "2018-05-15",
  "id_turma": 1,
  "nome_responsavel": "João Silva",
  "telefone_responsavel": "(11) 98765-4321",
  "email_responsavel": "joao.silva@email.com",
  "informacoes_adicionais": "Alérgica a amendoim"
}
```

### GET - Listar Todos os Alunos

**Endpoint:** `/alunos`

**Método:** `GET`

### GET - Buscar Aluno por ID

**Endpoint:** `/alunos/1`

**Método:** `GET`

**⚠️ Importante:** Apenas passe o ID na URL. Não é necessário enviar body.

### PUT - Atualizar Aluno

**Endpoint:** `/alunos/1`

**Método:** `PUT`

**Body (JSON):**
```json
{
  "nome_completo": "Maria Silva Oliveira",
  "data_nascimento": "2018-05-15",
  "id_turma": 2,
  "nome_responsavel": "João Silva",
  "telefone_responsavel": "(11) 98765-4321",
  "email_responsavel": "joao.silva@email.com",
  "informacoes_adicionais": "Alérgica a amendoim e leite"
}
```

### DELETE - Excluir Aluno

**Endpoint:** `/alunos/1`

**Método:** `DELETE`

**⚠️ Importante:** Apenas passe o ID na URL. Não é necessário enviar body.

## Turmas

### POST - Criar Turma

**Endpoint:** `/turmas`

**Método:** `POST`

**Body (JSON):**
```json
{
  "nome_turma": "Turma Infantil A",
  "id_professor": 1,
  "horario": "08:00 - 12:00"
}
```

### GET - Listar Todas as Turmas

**Endpoint:** `/turmas`

**Método:** `GET`

### GET - Buscar Turma por ID

**Endpoint:** `/turmas/1`

**Método:** `GET`

**⚠️ Importante:** Apenas passe o ID na URL. Não é necessário enviar body.

### PUT - Atualizar Turma

**Endpoint:** `/turmas/1`

**Método:** `PUT`

**Body (JSON):**
```json
{
  "nome_turma": "Turma Infantil B",
  "id_professor": 2,
  "horario": "13:00 - 17:00"
}
```

### DELETE - Excluir Turma

**Endpoint:** `/turmas/1`

**Método:** `DELETE`

**⚠️ Importante:** Apenas passe o ID na URL. Não é necessário enviar body.

## Professores

### POST - Criar Professor

**Endpoint:** `/professores`

**Método:** `POST`

**Body (JSON):**
```json
{
  "nome_completo": "Ana Souza",
  "data_nascimento": "1985-03-20",
  "telefone": "(11) 91234-5678",
  "email": "ana.souza@email.com",
  "data_contratacao": "2022-01-15"
}
```

### GET - Listar Todos os Professores

**Endpoint:** `/professores`

**Método:** `GET`

### GET - Buscar Professor por ID

**Endpoint:** `/professores/1`

**Método:** `GET`

**⚠️ Importante:** Apenas passe o ID na URL. Não é necessário enviar body.

### PUT - Atualizar Professor

**Endpoint:** `/professores/1`

**Método:** `PUT`

**Body (JSON):**
```json
{
  "nome_completo": "Ana Souza Lima",
  "data_nascimento": "1985-03-20",
  "telefone": "(11) 91234-5678",
  "email": "ana.souza@email.com",
  "data_contratacao": "2022-01-15"
}
```

### DELETE - Excluir Professor

**Endpoint:** `/professores/1`

**Método:** `DELETE`

**⚠️ Importante:** Apenas passe o ID na URL. Não é necessário enviar body.

## Atividades

### POST - Criar Atividade

**Endpoint:** `/atividades`

**Método:** `POST`

**Body (JSON):**
```json
{
  "nome_atividade": "Pintura com Guache",
  "descricao": "Atividade de pintura com tinta guache para desenvolver coordenação motora",
  "data_atividade": "2023-10-15",
  "id_turma": 1
}
```

### GET - Listar Todas as Atividades

**Endpoint:** `/atividades`

**Método:** `GET`

### GET - Buscar Atividade por ID

**Endpoint:** `/atividades/1`

**Método:** `GET`

**⚠️ Importante:** Apenas passe o ID na URL. Não é necessário enviar body.

### PUT - Atualizar Atividade

**Endpoint:** `/atividades/1`

**Método:** `PUT`

**Body (JSON):**
```json
{
  "nome_atividade": "Pintura com Guache e Colagem",
  "descricao": "Atividade de pintura com tinta guache e colagem para desenvolver coordenação motora",
  "data_atividade": "2023-10-16",
  "id_turma": 1
}
```

### DELETE - Excluir Atividade

**Endpoint:** `/atividades/1`

**Método:** `DELETE`

**⚠️ Importante:** Apenas passe o ID na URL. Não é necessário enviar body.

## Atividade-Aluno

### POST - Registrar Atividade para Aluno

**Endpoint:** `/atividade-aluno`

**Método:** `POST`

**Body (JSON):**
```json
{
  "id_atividade": 1,
  "id_aluno": 1,
  "observacoes": "Aluno participou com entusiasmo",
  "nota": "Excelente"
}
```

### GET - Listar Todas as Atividades-Aluno

**Endpoint:** `/atividade-aluno`

**Método:** `GET`

### GET - Buscar Atividade-Aluno por ID

**Endpoint:** `/atividade-aluno/1`

**Método:** `GET`

**⚠️ Importante:** Apenas passe o ID na URL. Não é necessário enviar body.

### PUT - Atualizar Atividade-Aluno

**Endpoint:** `/atividade-aluno/1`

**Método:** `PUT`

**Body (JSON):**
```json
{
  "id_atividade": 1,
  "id_aluno": 1,
  "observacoes": "Aluno participou com muito entusiasmo e criatividade",
  "nota": "Excelente"
}
```

### DELETE - Excluir Atividade-Aluno

**Endpoint:** `/atividade-aluno/1`

**Método:** `DELETE`

**⚠️ Importante:** Apenas passe o ID na URL. Não é necessário enviar body.

## Presenças

### POST - Registrar Presença

**Endpoint:** `/presencas`

**Método:** `POST`

**Body (JSON):**
```json
{
  "id_aluno": 1,
  "data_presenca": "2023-10-15",
  "presente": true,
  "observacao": "Chegou no horário"
}
```

### GET - Listar Todas as Presenças

**Endpoint:** `/presencas`

**Método:** `GET`

### GET - Buscar Presença por ID

**Endpoint:** `/presencas/1`

**Método:** `GET`

**⚠️ Importante:** Apenas passe o ID na URL. Não é necessário enviar body.

### PUT - Atualizar Presença

**Endpoint:** `/presencas/1`

**Método:** `PUT`

**Body (JSON):**
```json
{
  "id_aluno": 1,
  "data_presenca": "2023-10-15",
  "presente": false,
  "observacao": "Faltou por motivo de saúde"
}
```

### DELETE - Excluir Presença

**Endpoint:** `/presencas/1`

**Método:** `DELETE`

**⚠️ Importante:** Apenas passe o ID na URL. Não é necessário enviar body.

## Pagamentos

### POST - Registrar Pagamento

**Endpoint:** `/pagamentos`

**Método:** `POST`

**Body (JSON):**
```json
{
  "id_aluno": 1,
  "valor": 500.00,
  "data_vencimento": "2023-10-10",
  "data_pagamento": "2023-10-08",
  "status": "pago",
  "metodo_pagamento": "PIX",
  "descricao": "Mensalidade de Outubro/2023"
}
```

### GET - Listar Todos os Pagamentos

**Endpoint:** `/pagamentos`

**Método:** `GET`

### GET - Buscar Pagamento por ID

**Endpoint:** `/pagamentos/1`

**Método:** `GET`

**⚠️ Importante:** Apenas passe o ID na URL. Não é necessário enviar body.

### PUT - Atualizar Pagamento

**Endpoint:** `/pagamentos/1`

**Método:** `PUT`

**Body (JSON):**
```json
{
  "id_aluno": 1,
  "valor": 500.00,
  "data_vencimento": "2023-10-10",
  "data_pagamento": "2023-10-09",
  "status": "pago",
  "metodo_pagamento": "Cartão de Crédito",
  "descricao": "Mensalidade de Outubro/2023"
}
```

### DELETE - Excluir Pagamento

**Endpoint:** `/pagamentos/1`

**Método:** `DELETE`

**⚠️ Importante:** Apenas passe o ID na URL. Não é necessário enviar body.

## Usuários

### ⚠️ IMPORTANTE - Antes de testar o Login

**Antes de testar o endpoint de login, você DEVE criar um usuário primeiro!**

O sistema não possui usuários pré-cadastrados. Siga os passos:
1. Primeiro execute o `POST - Criar Usuário` (abaixo)
2. Depois teste o `POST - Login` com as mesmas credenciais

### POST - Login

**Endpoint:** `/login`

**Método:** `POST`

**Body (JSON):**
```json
{
  "nome_usuario": "admin",
  "senha": "senha123"
}
```

**⚠️ Lembre-se:** Use as mesmas credenciais que você criou no endpoint de criar usuário.

### POST - Criar Usuário

**Endpoint:** `/usuarios`

**Método:** `POST`

**Body (JSON):**
```json
{
  "nome_usuario": "admin",
  "senha": "senha123",
  "email": "admin@escola.com",
  "tipo": "administrador"
}
```

### GET - Listar Todos os Usuários

**Endpoint:** `/usuarios`

**Método:** `GET`

### GET - Buscar Usuário por ID

**Endpoint:** `/usuarios/1`

**Método:** `GET`

**⚠️ Importante:** Apenas passe o ID na URL. Não é necessário enviar body.

### PUT - Atualizar Usuário

**Endpoint:** `/usuarios/1`

**Método:** `PUT`

**Body (JSON):**
```json
{
  "nome_usuario": "admin",
  "senha": "novaSenha456",
  "email": "admin@escola.com",
  "tipo": "administrador"
}
```

### DELETE - Excluir Usuário

**Endpoint:** `/usuarios/1`

**Método:** `DELETE`

**⚠️ Importante:** Apenas passe o ID na URL. Não é necessário enviar body.