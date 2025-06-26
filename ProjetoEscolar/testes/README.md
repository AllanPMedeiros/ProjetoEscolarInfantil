# Testes Pytest - Projeto Escolar Infantil

Este diretório contém os testes pytest com mocks para todos os CRUDs do projeto escolar infantil.

## Estrutura dos Testes

- `test_pytest_mocks.py` - Todos os testes pytest com mocks
- `conftest.py` - Configuração das fixtures do pytest
- `pytest.ini` - Configuração do pytest

## Como Executar os Testes

### Executar todos os testes
```bash
cd testes
pytest test_pytest_mocks.py -v
```

### Executar teste específico
```bash
pytest test_pytest_mocks.py::TestPytestMocks::test_create_aluno -v
```

### Executar com relatório HTML
```bash
pytest test_pytest_mocks.py --html=report.html
```

## Cobertura dos Testes

Cada CRUD é testado com mocks:

- **Alunos** - CREATE, READ, UPDATE, DELETE, LIST (5 testes)
- **Professores** - CREATE, READ, UPDATE, DELETE, LIST (5 testes)
- **Turmas** - CREATE, LIST (2 testes)
- **Usuários** - CREATE, LIST (2 testes)
- **Atividades** - CREATE, LIST (2 testes)
- **Pagamentos** - CREATE, LIST (2 testes)
- **Presenças** - CREATE, LIST (2 testes)
- **Atividade_Aluno** - CREATE, LIST (2 testes)

**Total: 22 testes**

## Características dos Testes

- Utilizam **pytest** como framework
- Usam **mocks** para simular conexões com banco de dados
- Testam cenários de **sucesso**
- Verificam **códigos de status HTTP** apropriados
- São **rápidos** e **independentes**

## Dependências

- `pytest` (instalado automaticamente)
- `unittest.mock` (biblioteca padrão do Python)
- `flask` para testes de rotas

## Observações

- Os testes não fazem conexão real com o banco de dados
- Utilizam mocks para simular respostas do banco
- São testes rápidos focados na lógica de negócio
- Verificam se os CRUDs estão funcionando corretamente