DROP TABLE IF EXISTS atividade_aluno;
DROP TABLE IF EXISTS atividade;
DROP TABLE IF EXISTS presenca;
DROP TABLE IF EXISTS pagamento;
DROP TABLE IF EXISTS aluno;
DROP TABLE IF EXISTS turma;
DROP TABLE IF EXISTS professor;
DROP TABLE IF EXISTS usuario;

CREATE TABLE professor (
    id_professor INTEGER PRIMARY KEY,
    nome_completo VARCHAR(255) NOT NULL,
    email VARCHAR(100),
    telefone VARCHAR(20)
);

CREATE TABLE turma (
    id_turma INTEGER PRIMARY KEY,
    nome_turma VARCHAR(50) NOT NULL,
    id_professor INT,
    horario VARCHAR(100),
    FOREIGN KEY (id_professor) REFERENCES professor(id_professor)
);

CREATE TABLE aluno (
    id_aluno INTEGER PRIMARY KEY,
    nome_completo VARCHAR(255) NOT NULL,
    data_nascimento DATE NOT NULL,
    id_turma INT,
    nome_responsavel VARCHAR(255),
    telefone_responsavel VARCHAR(20),
    email_responsavel VARCHAR(100),
    informacoes_adicionais TEXT,
    endereco VARCHAR(255),  -- Adicionada a coluna endereco
    cidade VARCHAR(100),
    estado VARCHAR(100),
    cep VARCHAR(20),
    pais VARCHAR(100),
    telefone VARCHAR(20),
    FOREIGN KEY (id_turma) REFERENCES turma(id_turma)
);

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

CREATE TABLE presenca (
    id_presenca INTEGER PRIMARY KEY,
    id_aluno INT,
    data_presenca DATE NOT NULL,
    presente BOOLEAN,
    FOREIGN KEY (id_aluno) REFERENCES aluno(id_aluno)
);

CREATE TABLE atividade (
    id_atividade INTEGER PRIMARY KEY,
    descricao TEXT NOT NULL,
    data_realizacao DATE NOT NULL
);

CREATE TABLE atividade_aluno (
    id_atividade INT,
    id_aluno INT,
    PRIMARY KEY (id_atividade, id_aluno),
    FOREIGN KEY (id_atividade) REFERENCES atividade(id_atividade),
    FOREIGN KEY (id_aluno) REFERENCES aluno(id_aluno)
);

CREATE TABLE usuario (
    id_usuario INTEGER PRIMARY KEY,
    login VARCHAR(50) UNIQUE NOT NULL,
    senha VARCHAR(255) NOT NULL,
    nivel_acesso VARCHAR(20),
    id_professor INT,
    FOREIGN KEY (id_professor) REFERENCES professor(id_professor)
);

INSERT INTO professor (id_professor, nome_completo, email, telefone) VALUES 
(1, 'João Silva', 'joao@escola.com', '123456789'),
(2, 'Maria Santos', 'maria@escola.com', '987654321');

INSERT INTO turma (id_turma, nome_turma, id_professor, horario) VALUES 
(1, 'Turma A', 1, '08:00 - 10:00'),
(2, 'Turma B', 2, '10:00 - 12:00');

INSERT INTO aluno (id_aluno, nome_completo, data_nascimento, id_turma, nome_responsavel, telefone_responsavel, email_responsavel, endereco, cidade, estado, cep, pais, telefone) VALUES 
(1, 'Maria Oliveira', '2010-05-15', 1, 'Ana Oliveira', '987654321', 'ana@escola.com', 'Rua A, 123', 'São Paulo', 'SP', '12345-678', 'Brasil', '11987654321'),
(2, 'Pedro Almeida', '2011-03-20', 1, 'Carlos Almeida', '123456789', 'carlos@escola.com', 'Rua B, 456', 'Rio de Janeiro', 'RJ', '23456-789', 'Brasil', '21987654321'),
(3, 'Lucas Pereira', '2010-07-30', 2, 'Fernanda Pereira', '456789123', 'fernanda@escola.com', 'Rua C, 789', 'Belo Horizonte', 'MG', '34567-890', 'Brasil', '31987654321');

INSERT INTO pagamento (id_pagamento, id_aluno, data_pagamento, valor_pago, forma_pagamento, referencia, status) VALUES 
(1, 1, '2023-03-01', 200.00, 'Transferência', 'Mensalidade Março', 'Pago'),
(2, 2, '2023-03-01', 200.00, 'Cartão de Crédito', 'Mensalidade Março', 'Pendente');

INSERT INTO presenca (id_presenca, id_aluno, data_presenca, presente) VALUES 
(1, 1, '2023-03-01', TRUE),
(2, 2, '2023-03-01', FALSE);

INSERT INTO atividade (id_atividade, descricao, data_realizacao) VALUES 
(1, 'Atividade de Matemática', '2023-03-15'),
(2, 'Atividade de Português', '2023-03-20');

INSERT INTO atividade_aluno (id_atividade, id_aluno) VALUES 
(1, 1),
(1, 2),
(2, 1),
(2, 3);

INSERT INTO usuario (id_usuario, login, senha, nivel_acesso, id_professor) VALUES 
(1, 'usuario1', 'senha_hash_1', 'professor', 1),
(2, 'usuario2', 'senha_hash_2', 'administrador', NULL);