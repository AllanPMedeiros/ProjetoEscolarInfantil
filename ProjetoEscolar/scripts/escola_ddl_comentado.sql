
-- TABELA: professor
-- Um professor pode lecionar em várias turmas (1:N)
CREATE TABLE professor (
    id_professor INTEGER PRIMARY KEY,
    nome_completo VARCHAR(255) NOT NULL,
    email VARCHAR(100),
    telefone VARCHAR(20)
);

-- TABELA: turma
-- Cada turma pertence a um professor (N:1)
-- Uma turma pode ter vários alunos (1:N)
CREATE TABLE turma (
    id_turma INTEGER PRIMARY KEY,
    nome_turma VARCHAR(50) NOT NULL,
    id_professor INT,
    horario VARCHAR(100),
    FOREIGN KEY (id_professor) REFERENCES professor(id_professor)
);

-- TABELA: aluno
-- Cada aluno pertence a uma turma (N:1)
-- Um aluno pode ter vários pagamentos, presenças e atividades (1:N)
CREATE TABLE aluno (
    id_aluno INTEGER PRIMARY KEY,
    nome_completo VARCHAR(255) NOT NULL,
    data_nascimento DATE NOT NULL,
    id_turma INT,
    nome_responsavel VARCHAR(255),
    telefone_responsavel VARCHAR(20),
    email_responsavel VARCHAR(100),
    informacoes_adicionais TEXT,
    FOREIGN KEY (id_turma) REFERENCES turma(id_turma)
);

-- TABELA: pagamento
-- Cada pagamento está ligado a um único aluno (N:1)
CREATE TABLE pagamento (
    id_pagamento INTEGER PRIMARY KEY,
    id_aluno INT,
    data_pagamento DATE NOT NULL,
    valor_pago DECIMAL(10, 2) NOT NULL,
    forma_pagamento VARCHAR(50),
    referencia VARCHAR(100),
    status VARCHAR(20),
    FOREIGN KEY (id_aluno) REFERENCES aluno(id_aluno)
);

-- TABELA: presenca
-- Cada presença está ligada a um único aluno (N:1)
CREATE TABLE presenca (
    id_presenca INTEGER PRIMARY KEY,
    id_aluno INT,
    data_presenca DATE NOT NULL,
    presente BOOLEAN,
    FOREIGN KEY (id_aluno) REFERENCES aluno(id_aluno)
);

-- TABELA: atividade
-- Cada atividade pode estar relacionada a vários alunos (N:N via atividade_aluno)
CREATE TABLE atividade (
    id_atividade INTEGER PRIMARY KEY,
    descricao TEXT NOT NULL,
    data_realizacao DATE NOT NULL
);

-- TABELA: atividade_aluno
-- Tabela de associação (N:N entre aluno e atividade)
CREATE TABLE atividade_aluno (
    id_atividade INT,
    id_aluno INT,
    PRIMARY KEY (id_atividade, id_aluno),
    FOREIGN KEY (id_atividade) REFERENCES atividade(id_atividade),
    FOREIGN KEY (id_aluno) REFERENCES aluno(id_aluno)
);

-- TABELA: usuario
-- Cada usuário pode estar associado a um professor (N:1)
CREATE TABLE usuario (
    id_usuario INTEGER PRIMARY KEY,
    login VARCHAR(50) UNIQUE NOT NULL,
    senha VARCHAR(255) NOT NULL,
    nivel_acesso VARCHAR(20),
    id_professor INT,
    FOREIGN KEY (id_professor) REFERENCES professor(id_professor)
);