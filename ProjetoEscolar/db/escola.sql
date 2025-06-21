DROP TABLE IF EXISTS atividade_aluno;
DROP TABLE IF EXISTS atividade;
DROP TABLE IF EXISTS presenca;
DROP TABLE IF EXISTS pagamento;
DROP TABLE IF EXISTS aluno;
DROP TABLE IF EXISTS turma;
DROP TABLE IF EXISTS usuario;
DROP TABLE IF EXISTS professor;

CREATE TABLE professor (
    id_professor SERIAL PRIMARY KEY,
    nome_completo VARCHAR(255) NOT NULL,
    email VARCHAR(100),
    telefone VARCHAR(20)
);

CREATE TABLE turma (
    id_turma SERIAL PRIMARY KEY,
    nome_turma VARCHAR(50) NOT NULL,
    id_professor INT,
    horario VARCHAR(100),
    FOREIGN KEY (id_professor) REFERENCES professor(id_professor)
);

CREATE TABLE aluno (
    id_aluno SERIAL PRIMARY KEY,
    nome_completo VARCHAR(255) NOT NULL,
    data_nascimento DATE NOT NULL,
    id_turma INT,
    nome_responsavel VARCHAR(255),
    telefone_responsavel VARCHAR(20),
    email_responsavel VARCHAR(100),
    informacoes_adicionais TEXT,
    FOREIGN KEY (id_turma) REFERENCES turma(id_turma)
);

CREATE TABLE pagamento (
    id_pagamento SERIAL PRIMARY KEY,
    id_aluno INT,
    data_pagamento DATE NOT NULL,
    valor_pago DECIMAL(10, 2) NOT NULL,
    forma_pagamento VARCHAR(50),
    referencia VARCHAR(100),
    status VARCHAR(20),
    FOREIGN KEY (id_aluno) REFERENCES aluno(id_aluno)
);

CREATE TABLE presenca (
    id_presenca SERIAL PRIMARY KEY,
    id_aluno INT,
    data_presenca DATE NOT NULL,
    presente BOOLEAN,
    FOREIGN KEY (id_aluno) REFERENCES aluno(id_aluno)
);

CREATE TABLE atividade (
    id_atividade SERIAL PRIMARY KEY,
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
    id_usuario SERIAL PRIMARY KEY,
    login VARCHAR(50) UNIQUE NOT NULL,
    senha VARCHAR(255) NOT NULL,
    nivel_acesso VARCHAR(20),
    id_professor INT,
    FOREIGN KEY (id_professor) REFERENCES professor(id_professor)
);

-- Inserir dados na tabela professor
INSERT INTO professor (nome_completo, email, telefone) VALUES 
('João Silva', 'joao.silva@escola.com', '(11) 98765-4321'),
('Maria Santos', 'maria.santos@escola.com', '(11) 91234-5678'),
('Carlos Oliveira', 'carlos.oliveira@escola.com', '(11) 99876-5432'),
('Ana Pereira', 'ana.pereira@escola.com', '(11) 92345-6789');

-- Inserir dados na tabela turma
INSERT INTO turma (nome_turma, id_professor, horario) VALUES 
('Turma A - Maternal', 1, '08:00 - 12:00'),
('Turma B - Jardim I', 2, '13:00 - 17:00'),
('Turma C - Jardim II', 3, '08:00 - 12:00'),
('Turma D - Pré-escola', 4, '13:00 - 17:00');

-- Inserir dados na tabela aluno
INSERT INTO aluno (nome_completo, data_nascimento, id_turma, nome_responsavel, telefone_responsavel, email_responsavel, informacoes_adicionais) VALUES 
('Lucas Mendes', '2019-03-15', 1, 'Roberto Mendes', '(11) 97777-8888', 'roberto@email.com', 'Alergia a amendoim'),
('Julia Costa', '2019-05-20', 1, 'Mariana Costa', '(11) 96666-7777', 'mariana@email.com', 'Intolerância a lactose'),
('Pedro Almeida', '2018-07-10', 2, 'Fernanda Almeida', '(11) 95555-6666', 'fernanda@email.com', 'Sem Informações'),
('Sofia Rodrigues', '2018-09-25', 2, 'Ricardo Rodrigues', '(11) 94444-5555', 'ricardo@email.com', 'Asma'),
('Miguel Santos', '2017-11-30', 3, 'Patricia Santos', '(11) 93333-4444', 'patricia@email.com', 'Sem Informações'),
('Laura Oliveira', '2017-02-14', 3, 'Eduardo Oliveira', '(11) 92222-3333', 'eduardo@email.com', 'Alergia a picada de insetos'),
('Gabriel Lima', '2016-04-05', 4, 'Cristina Lima', '(11) 91111-2222', 'cristina@email.com', 'Sem Informações'),
('Beatriz Ferreira', '2016-08-18', 4, 'Marcelo Ferreira', '(11) 90000-1111', 'marcelo@email.com', 'Alergia a corantes');

-- Inserir dados na tabela pagamento
INSERT INTO pagamento (id_aluno, data_pagamento, valor_pago, forma_pagamento, referencia, status) VALUES 
(1, '2023-03-05', 500.00, 'Cartão de Crédito', 'Mensalidade Março/2023', 'Pago'),
(2, '2023-03-10', 500.00, 'Transferência', 'Mensalidade Março/2023', 'Pago'),
(3, '2023-03-07', 550.00, 'Boleto', 'Mensalidade Março/2023', 'Pago'),
(4, '2023-03-15', 550.00, 'PIX', 'Mensalidade Março/2023', 'Pago'),
(5, '2023-03-08', 600.00, 'Cartão de Débito', 'Mensalidade Março/2023', 'Pago'),
(6, '2023-03-12', 600.00, 'Transferência', 'Mensalidade Março/2023', 'Pago'),
(7, '2023-03-20', 650.00, 'PIX', 'Mensalidade Março/2023', 'Pendente'),
(8, '2023-03-18', 650.00, 'Boleto', 'Mensalidade Março/2023', 'Pendente');

-- Inserir dados na tabela presenca
INSERT INTO presenca (id_aluno, data_presenca, presente) VALUES 
(1, '2023-03-01', TRUE),
(2, '2023-03-01', TRUE),
(3, '2023-03-01', TRUE),
(4, '2023-03-01', FALSE),
(5, '2023-03-01', TRUE),
(6, '2023-03-01', TRUE),
(7, '2023-03-01', FALSE),
(8, '2023-03-01', TRUE),
(1, '2023-03-02', TRUE),
(2, '2023-03-02', TRUE),
(3, '2023-03-02', FALSE),
(4, '2023-03-02', TRUE),
(5, '2023-03-02', TRUE),
(6, '2023-03-02', FALSE),
(7, '2023-03-02', TRUE),
(8, '2023-03-02', TRUE);

-- Inserir dados na tabela atividade
INSERT INTO atividade (descricao, data_realizacao) VALUES 
('Atividade de Pintura - Cores Primárias', '2023-03-10'),
('Contação de História - Os Três Porquinhos', '2023-03-15'),
('Atividade de Coordenação Motora', '2023-03-20'),
('Introdução aos Números', '2023-03-25');

-- Inserir dados na tabela atividade_aluno
INSERT INTO atividade_aluno (id_atividade, id_aluno) VALUES 
(1, 1), (1, 2), (1, 3), (1, 4),
(2, 1), (2, 2), (2, 5), (2, 6),
(3, 3), (3, 4), (3, 7), (3, 8),
(4, 5), (4, 6), (4, 7), (4, 8);

-- Inserir dados na tabela usuario
INSERT INTO usuario (login, senha, nivel_acesso, id_professor) VALUES 
('admin', '$2a$12$1XT8jNxS8V8z1v3Bq0WFTuQCLMwXRYhPcMXlA7jiFU1UkNGgGMKAy', 'administrador', NULL), -- senha: admin123
('joao.silva', '$2a$12$QOpFRTBLMqA.KpQOUPDQDOkZPRsGkHRqWfAT9nD0OP1MaYwJJk4tS', 'professor', 1), -- senha: joao123
('maria.santos', '$2a$12$QOpFRTBLMqA.KpQOUPDQDOkZPRsGkHRqWfAT9nD0OP1MaYwJJk4tS', 'professor', 2), -- senha: maria123
('carlos.oliveira', '$2a$12$QOpFRTBLMqA.KpQOUPDQDOkZPRsGkHRqWfAT9nD0OP1MaYwJJk4tS', 'professor', 3), -- senha: carlos123
('ana.pereira', '$2a$12$QOpFRTBLMqA.KpQOUPDQDOkZPRsGkHRqWfAT9nD0OP1MaYwJJk4tS', 'professor', 4); -- senha: ana123

