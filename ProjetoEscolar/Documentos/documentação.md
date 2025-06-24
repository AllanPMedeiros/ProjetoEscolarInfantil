# Justificativa do Modelo de Dados

Este documento apresenta as razões e critérios adotados para a definição de cada tabela, coluna e relacionamentos do banco de dados desenvolvido para o sistema de gestão escolar.

---

## 1. Tabela `professor`

* **Propósito**: Armazenar os dados básicos dos professores que ministram aulas.
* **Colunas**:

  * `id_professor` (PK): Chave primária numérica autoexplicativa, para identificação única de cada professor.
  * `nome_completo` (VARCHAR): Nome completo do professor. Campo obrigatório para identificação clara.
  * `email` (VARCHAR): Contato eletrónico. Útil para notificações e recuperação de senha.
  * `telefone` (VARCHAR): Contato telefônico. Opcional, mas importante para emergências.

## 2. Tabela `turma`

* **Propósito**: Representar turmas ou classes formadas por alunos e ministradas por professores.

* **Colunas**:

  * `id_turma` (PK): Identificador único da turma.
  * `nome_turma` (VARCHAR): Nome ou código da turma (ex.: "3º Ano A"). Campo obrigatório.
  * `id_professor` (FK): Referência ao professor responsável. Garante integridade referencial e facilita consultas de aulas por docente.
  * `horario` (VARCHAR): Descrição do turno ou horário (ex.: "Seg/Qua/Sex - 14h às 16h").

* **Relacionamento**:

  * **1\:N** de `professor` para `turma`: um professor pode lecionar em várias turmas.

## 3. Tabela `aluno`

* **Propósito**: Guardar informações dos alunos matriculados.

* **Colunas**:

  * `id_aluno` (PK): Identificador único do aluno.
  * `nome_completo` (VARCHAR): Nome completo para identificação oficial.
  * `data_nascimento` (DATE): Data de nascimento para controle etário.
  * `id_turma` (FK): Associação à turma matriculada.
  * `nome_responsavel`, `telefone_responsavel`, `email_responsavel`: Contatos de responsáveis em caso de menores.
  * `informacoes_adicionais` (TEXT): Anotações extras (alergias, necessidades especiais etc.).
  * Dados de localização (`endereco`, `cidade`, `estado`, `cep`, `pais`): Para correspondências e relatórios regionais.
  * `telefone` (VARCHAR): Contato direto do aluno ou responsável.

* **Relacionamentos**:

  * **1\:N** de `turma` para `aluno`: uma turma agrupa vários alunos.
  * **1\:N** de `aluno` para `pagamento`, `presenca` e `atividade_aluno`.

## 4. Tabela `pagamento`

* **Propósito**: Registrar transações financeiras de cada aluno.

* **Colunas**:

  * `id_pagamento` (PK): Identificador único do pagamento.
  * `id_aluno` (FK): Aluno que realizou o pagamento.
  * `data_pagamento` (DATE): Data da transação.
  * `valor_pago` (DECIMAL): Montante pago, com precisão para valores monetários.
  * `forma_pagamento` (VARCHAR): Meio usado (cartão, boleto, dinheiro etc.).
  * `referencia` (VARCHAR): Número ou código de referência bancária.
  * `status` (VARCHAR): Situação do pagamento (efetuado, pendente, cancelado etc.).

* **Relacionamento**:

  * **1\:N** de `aluno` para `pagamento`.

## 5. Tabela `presenca`

* **Propósito**: Monitorar a frequência dos alunos.

* **Colunas**:

  * `id_presenca` (PK): Identificador único do registro.
  * `id_aluno` (FK): Aluno avaliado.
  * `data_presenca` (DATE): Data da aula.
  * `presente` (BOOLEAN): Indicador de presença ou falta.

* **Relacionamento**:

  * **1\:N** de `aluno` para `presenca`.

## 6. Tabela `atividade`

* **Propósito**: Definir atividades ou avaliações programadas.
* **Colunas**:

  * `id_atividade` (PK): Identificador da atividade.
  * `descricao` (TEXT): Detalhes sobre a tarefa ou avaliação.
  * `data_realizacao` (DATE): Data prevista ou realizada.

## 7. Tabela `atividade_aluno`

* **Propósito**: Relacionar alunos às atividades realizadas, permitindo múltiplas participações.

* **Chave primária composta** (`id_atividade`, `id_aluno`): Garante unicidade de cada par atividade-aluno.

* **Relacionamento**:

  * **N\:N** entre `aluno` e `atividade`, implementado por esta tabela de junção.

## 8. Tabela `usuario`

* **Propósito**: Controlar logins e níveis de acesso ao sistema.

* **Colunas**:

  * `id_usuario` (PK): Identificador do usuário do sistema.
  * `login` (VARCHAR, UNIQUE): Nome de usuário único.
  * `senha` (VARCHAR): Hash de senha para segurança.
  * `nivel_acesso` (VARCHAR): Permissões (administrador, professor, recepção etc.).
  * `id_professor` (FK): Associação opcional ao professor para perfis vinculados.

* **Relacionamento**:

  * **1\:N** de `professor` para `usuario`: um professor pode ter múltiplos acessos.

---

Essas escolhas objetivam garantir integridade dos dados, rastreabilidade das operações e flexibilidade para futuras expansões (ex.: incluir horários mais complexos, novos tipos de atividades ou níveis de acesso).
