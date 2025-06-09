import pytest
from unittest.mock import patch, MagicMock
import json
import sys
import os

# Adiciona o diretório raiz do projeto ao sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Importe diretamente o Blueprint e crie uma aplicação de teste
from App.crudProfessores import app as professores_bp
from flask import Flask

@pytest.fixture
def app():
    """Cria uma aplicação Flask para testes"""
    test_app = Flask(__name__)
    test_app.config.update({
        "TESTING": True,
    })
    # Registra o Blueprint na aplicação
    test_app.register_blueprint(professores_bp)
    return test_app

@pytest.fixture
def client(app):
    """Cria um cliente de teste"""
    return app.test_client()

@patch('App.Utils.bd.create_connection')
def test_create_professor_success(mock_create_connection, client):
    # Configurar o mock
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_create_connection.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor

    # Dados de teste
    test_data = {
        'nome_completo': 'Professor Teste',
        'email': 'teste@email.com',
        'telefone': '(11) 1234-5678'
    }

    # Enviar requisição
    response = client.post('/professores', 
                          data=json.dumps(test_data),
                          content_type='application/json')

    # Verificar resultados
    assert response.status_code == 201
    assert b'Professor criado com sucesso' in response.data
    
    # Verificar se o mock foi chamado corretamente
    mock_cursor.execute.assert_called_once()
    mock_conn.commit.assert_called_once()

@patch('App.Utils.bd.create_connection')
def test_read_professor_success(mock_create_connection, client):
    # Configurar o mock
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_create_connection.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor
    
    # Configurar o resultado do fetchone
    professor_mock = (1, 'Professor Teste', 'teste@email.com', '(11) 1234-5678')
    mock_cursor.fetchone.return_value = professor_mock

    # Enviar requisição
    response = client.get('/professores/1')

    # Verificar resultados
    assert response.status_code == 200
    response_data = json.loads(response.data)
    assert response_data['nome_completo'] == 'Professor Teste'
    assert response_data['email'] == 'teste@email.com'
    
    # Verificar se o mock foi chamado corretamente
    mock_cursor.execute.assert_called_once()

@patch('App.Utils.bd.create_connection')
def test_read_professor_not_found(mock_create_connection, client):
    # Configurar o mock
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_create_connection.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor
    
    # Configurar o resultado do fetchone como None (não encontrado)
    mock_cursor.fetchone.return_value = None

    # Enviar requisição
    response = client.get('/professores/999')

    # Verificar resultados
    assert response.status_code == 404
    assert b'Professor n\\u00e3o encontrado' in response.data

@patch('App.Utils.bd.create_connection')
def test_read_all_professores(mock_create_connection, client):
    # Configurar o mock
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_create_connection.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor
    
    # Configurar o resultado do fetchall
    professores_mock = [
        (1, 'Professor A', 'a@email.com', '(11) 1111-1111'),
        (2, 'Professor B', 'b@email.com', '(22) 2222-2222')
    ]
    mock_cursor.fetchall.return_value = professores_mock

    # Enviar requisição
    response = client.get('/professores')

    # Verificar resultados
    assert response.status_code == 200
    response_data = json.loads(response.data)
    assert len(response_data) == 2
    assert response_data[0]['nome_completo'] == 'Professor A'
    assert response_data[1]['nome_completo'] == 'Professor B'

@patch('App.Utils.bd.create_connection')
def test_update_professor_success(mock_create_connection, client):
    # Configurar o mock
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_create_connection.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor
    
    # Configurar o rowcount para indicar atualização bem-sucedida
    mock_cursor.rowcount = 1

    # Dados de teste
    update_data = {
        'nome_completo': 'Professor Atualizado',
        'email': 'atualizado@email.com',
        'telefone': '(33) 3333-3333'
    }

    # Enviar requisição
    response = client.put('/professores/1', 
                         data=json.dumps(update_data),
                         content_type='application/json')

    # Verificar resultados
    assert response.status_code == 200
    assert b'Professor atualizado com sucesso' in response.data
    
    # Verificar se o mock foi chamado corretamente
    mock_cursor.execute.assert_called_once()
    mock_conn.commit.assert_called_once()

@patch('App.Utils.bd.create_connection')
def test_delete_professor_success(mock_create_connection, client):
    # Configurar o mock
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_create_connection.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor
    
    # Configurar o rowcount para indicar exclusão bem-sucedida
    mock_cursor.rowcount = 1

    # Enviar requisição
    response = client.delete('/professores/1')

    # Verificar resultados
    assert response.status_code == 200
    assert b'Professor deletado com sucesso' in response.data
    
    # Verificar se o mock foi chamado corretamente
    mock_cursor.execute.assert_called_once()
    mock_conn.commit.assert_called_once()

@patch('App.Utils.bd.create_connection')
def test_connection_error(mock_create_connection, client):
    # Simular falha na conexão
    mock_create_connection.return_value = None

    # Enviar requisição
    response = client.get('/professores')

    # Verificar resultados - ajuste conforme necessário baseado na implementação atual
    assert response.status_code in [400, 500]  # Pode ser 400 ou 500 dependendo da implementação