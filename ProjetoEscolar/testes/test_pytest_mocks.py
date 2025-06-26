from unittest.mock import patch, MagicMock
from datetime import datetime

class TestPytestMocks:
    
    # TESTES ALUNOS
    @patch('App.crudAlunos.create_connection')
    def test_create_aluno(self, mock_conn, client):
        mock_cursor = MagicMock()
        mock_conn.return_value.cursor.return_value = mock_cursor
        mock_cursor.fetchone.return_value = [1]
        
        data = {'nome_completo': 'João Silva', 'data_nascimento': '2015-05-10'}
        response = client.post('/alunos', json=data)
        assert response.status_code == 201

    @patch('App.crudAlunos.create_connection')
    def test_read_aluno(self, mock_conn, client):
        mock_cursor = MagicMock()
        mock_conn.return_value.cursor.return_value = mock_cursor
        mock_cursor.fetchone.return_value = [1, 'João Silva', datetime(2015, 5, 10), 1, 'Maria', '123', 'maria@email.com', 'Info']
        
        response = client.get('/alunos/1')
        assert response.status_code == 200

    @patch('App.crudAlunos.create_connection')
    def test_update_aluno(self, mock_conn, client):
        mock_cursor = MagicMock()
        mock_conn.return_value.cursor.return_value = mock_cursor
        mock_cursor.rowcount = 1
        
        data = {'nome_completo': 'João Atualizado'}
        response = client.put('/alunos/1', json=data)
        assert response.status_code == 200

    @patch('App.crudAlunos.create_connection')
    def test_delete_aluno(self, mock_conn, client):
        mock_cursor = MagicMock()
        mock_conn.return_value.cursor.return_value = mock_cursor
        mock_cursor.fetchone.side_effect = [[1], [0]]
        
        response = client.delete('/alunos/1')
        assert response.status_code == 200

    @patch('App.crudAlunos.create_connection')
    def test_list_alunos(self, mock_conn, client):
        mock_cursor = MagicMock()
        mock_conn.return_value.cursor.return_value = mock_cursor
        mock_cursor.fetchall.return_value = [[1, 'João', datetime(2015, 5, 10), 1, 'Maria', '123', 'maria@email.com', 'Info']]
        
        response = client.get('/alunos')
        assert response.status_code == 200

    # TESTES PROFESSORES
    @patch('App.crudProfessores.create_connection')
    def test_create_professor(self, mock_conn, client):
        mock_cursor = MagicMock()
        mock_conn.return_value.cursor.return_value = mock_cursor
        mock_cursor.fetchone.return_value = [1]
        
        data = {'nome_completo': 'Prof. Maria', 'email': 'maria@escola.com'}
        response = client.post('/professores', json=data)
        assert response.status_code == 201

    @patch('App.crudProfessores.create_connection')
    def test_read_professor(self, mock_conn, client):
        mock_cursor = MagicMock()
        mock_conn.return_value.cursor.return_value = mock_cursor
        mock_cursor.fetchone.return_value = [1, 'Prof. Maria', 'maria@escola.com', '11999999999']
        
        response = client.get('/professores/1')
        assert response.status_code == 200

    @patch('App.crudProfessores.create_connection')
    def test_update_professor(self, mock_conn, client):
        mock_cursor = MagicMock()
        mock_conn.return_value.cursor.return_value = mock_cursor
        mock_cursor.rowcount = 1
        
        data = {'nome_completo': 'Prof. Maria Silva'}
        response = client.put('/professores/1', json=data)
        assert response.status_code == 200

    @patch('App.crudProfessores.create_connection')
    def test_delete_professor(self, mock_conn, client):
        mock_cursor = MagicMock()
        mock_conn.return_value.cursor.return_value = mock_cursor
        mock_cursor.fetchone.return_value = [1]
        
        response = client.delete('/professores/1')
        assert response.status_code == 200

    @patch('App.crudProfessores.create_connection')
    def test_list_professores(self, mock_conn, client):
        mock_cursor = MagicMock()
        mock_conn.return_value.cursor.return_value = mock_cursor
        mock_cursor.fetchall.return_value = [[1, 'Prof. Maria', 'maria@escola.com', '11999999999']]
        
        response = client.get('/professores')
        assert response.status_code == 200

    # TESTES TURMAS
    @patch('App.crudTurmas.create_connection')
    def test_create_turma(self, mock_conn, client):
        mock_cursor = MagicMock()
        mock_conn.return_value.cursor.return_value = mock_cursor
        mock_cursor.fetchone.side_effect = [[1], [1]]
        
        data = {'nome_turma': 'Turma A'}
        response = client.post('/turmas', json=data)
        assert response.status_code == 201

    @patch('App.crudTurmas.create_connection')
    def test_list_turmas(self, mock_conn, client):
        mock_cursor = MagicMock()
        mock_conn.return_value.cursor.return_value = mock_cursor
        mock_cursor.fetchall.return_value = [[1, 'Turma A', 1, '08:00-12:00', 'Prof. Maria']]
        
        response = client.get('/turmas')
        assert response.status_code == 200

    # TESTES USUARIOS
    @patch('App.crudUsuarios.create_connection')
    def test_create_usuario(self, mock_conn, client):
        mock_cursor = MagicMock()
        mock_conn.return_value.cursor.return_value = mock_cursor
        mock_cursor.fetchone.side_effect = [[0], [1]]
        
        data = {'login': 'admin', 'senha': 'senha123'}
        response = client.post('/usuarios', json=data)
        assert response.status_code == 201

    @patch('App.crudUsuarios.create_connection')
    def test_list_usuarios(self, mock_conn, client):
        mock_cursor = MagicMock()
        mock_conn.return_value.cursor.return_value = mock_cursor
        mock_cursor.fetchall.return_value = [[1, 'admin', 'admin', 1]]
        
        response = client.get('/usuarios')
        assert response.status_code == 200

    # TESTES ATIVIDADES
    @patch('App.crudAtividades.create_connection')
    def test_create_atividade(self, mock_conn, client):
        mock_cursor = MagicMock()
        mock_conn.return_value.cursor.return_value = mock_cursor
        mock_cursor.fetchone.return_value = [1]
        
        data = {'descricao': 'Atividade de Matemática', 'data_realizacao': '2024-01-15'}
        response = client.post('/atividades', json=data)
        assert response.status_code == 201

    @patch('App.crudAtividades.create_connection')
    def test_list_atividades(self, mock_conn, client):
        mock_cursor = MagicMock()
        mock_conn.return_value.cursor.return_value = mock_cursor
        mock_cursor.fetchall.return_value = [[1, 'Atividade de Matemática', '2024-01-15']]
        
        response = client.get('/atividades')
        assert response.status_code == 200

    # TESTES PAGAMENTOS
    @patch('App.crudPagamentos.create_connection')
    def test_create_pagamento(self, mock_conn, client):
        mock_cursor = MagicMock()
        mock_conn.return_value.cursor.return_value = mock_cursor
        mock_cursor.fetchone.side_effect = [[1], [1]]
        
        data = {'id_aluno': 1, 'data_pagamento': '2024-01-15', 'valor_pago': 150.00}
        response = client.post('/pagamentos', json=data)
        assert response.status_code == 201

    @patch('App.crudPagamentos.create_connection')
    def test_list_pagamentos(self, mock_conn, client):
        mock_cursor = MagicMock()
        mock_conn.return_value.cursor.return_value = mock_cursor
        mock_cursor.fetchall.return_value = [[1, 1, '2024-01-15', 150.00, 'PIX', 'REF001', 'Pago']]
        
        response = client.get('/pagamentos')
        assert response.status_code == 200

    # TESTES PRESENCAS
    @patch('App.crudPresencas.create_connection')
    def test_create_presenca(self, mock_conn, client):
        mock_cursor = MagicMock()
        mock_conn.return_value.cursor.return_value = mock_cursor
        mock_cursor.fetchone.side_effect = [[1], [0], [1]]
        
        data = {'id_aluno': 1, 'data_presenca': '2024-01-15', 'presente': True}
        response = client.post('/presencas', json=data)
        assert response.status_code == 201

    @patch('App.crudPresencas.create_connection')
    def test_list_presencas(self, mock_conn, client):
        mock_cursor = MagicMock()
        mock_conn.return_value.cursor.return_value = mock_cursor
        mock_cursor.fetchall.return_value = [[1, 1, '2024-01-15', True]]
        
        response = client.get('/presencas')
        assert response.status_code == 200

    # TESTES ATIVIDADE_ALUNO
    @patch('App.crudAtividade_Aluno.create_connection')
    def test_create_atividade_aluno(self, mock_conn, client):
        mock_cursor = MagicMock()
        mock_conn.return_value.cursor.return_value = mock_cursor
        
        data = {'id_atividade': 1, 'id_aluno': 1}
        response = client.post('/atividades_alunos', json=data)
        assert response.status_code == 201

    @patch('App.crudAtividade_Aluno.create_connection')
    def test_list_atividades_alunos(self, mock_conn, client):
        mock_cursor = MagicMock()
        mock_conn.return_value.cursor.return_value = mock_cursor
        mock_cursor.fetchall.return_value = [[1, 1]]
        
        response = client.get('/atividades_alunos')
        assert response.status_code == 200