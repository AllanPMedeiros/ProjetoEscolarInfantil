from flask import Flask, jsonify, request
from flasgger import Swagger, swag_from

app = Flask(__name__)
swagger = Swagger(app)

@app.route('/alunos', methods=['POST'])
@swag_from({
    'tags': ['Alunos'],
    'description': 'Cria um novo aluno.',
    'parameters': [{
        'name': 'body',
        'in': 'body',
        'required': True,
        'schema': {
            'type': 'object',
            'properties': {
                'aluno_id': {'type': 'string'},
                'nome': {'type': 'string'},
                'endereco': {'type': 'string'},
                'cidade': {'type': 'string'},
                'estado': {'type': 'string'},
                'cep': {'type': 'string'},
                'pais': {'type': 'string'},
                'telefone': {'type': 'string'}
            },
            'example': {
                'aluno_id': '123',
                'nome': 'João Silva',
                'endereco': 'Rua A, 123',
                'cidade': 'São Paulo',
                'estado': 'SP',
                'cep': '01000-000',
                'pais': 'Brasil',
                'telefone': '(11) 99999-9999'
            }
        }
    }],
    'responses': {
        201: {'description': 'Aluno criado com sucesso'},
        400: {'description': 'Erro na requisição'}
    }
})
def create_aluno():
    data = request.get_json()
    return jsonify({"message": "Aluno criado com sucesso"}), 201

@app.route('/alunos/<string:aluno_id>', methods=['GET'])
@swag_from({
    'tags': ['Alunos'],
    'description': 'Busca um aluno pelo ID.',
    'parameters': [{
        'name': 'aluno_id',
        'in': 'path',
        'required': True,
        'type': 'string'
    }],
    'responses': {
        200: {
            'description': 'Dados do aluno',
            'examples': {
                'application/json': {
                    "aluno_id": "123",
                    "nome": "João Silva",
                    "endereco": "Rua A, 123",
                    "cidade": "São Paulo",
                    "estado": "SP",
                    "cep": "01000-000",
                    "pais": "Brasil",
                    "telefone": "(11) 99999-9999"
                }
            }
        },
        404: {'description': 'Aluno não encontrado'}
    }
})
def read_aluno(aluno_id):
    return jsonify({
        "aluno_id": aluno_id,
        "nome": "João Silva",
        "endereco": "Rua A, 123",
        "cidade": "São Paulo",
        "estado": "SP",
        "cep": "01000-000",
        "pais": "Brasil",
        "telefone": "(11) 99999-9999"
    }), 200

@app.route('/alunos', methods=['GET'])
@swag_from({
    'tags': ['Alunos'],
    'description': 'Lista todos os alunos cadastrados.',
    'responses': {
        200: {
            'description': 'Lista de alunos',
            'examples': {
                'application/json': [
                    {
                        "aluno_id": "123",
                        "nome": "João Silva",
                        "endereco": "Rua A, 123",
                        "cidade": "São Paulo",
                        "estado": "SP",
                        "cep": "01000-000",
                        "pais": "Brasil",
                        "telefone": "(11) 99999-9999"
                    }
                ]
            }
        }
    }
})
def list_alunos():
    return jsonify([{  # Simulando resposta
        "aluno_id": "123",
        "nome": "João Silva",
        "endereco": "Rua A, 123",
        "cidade": "São Paulo",
        "estado": "SP",
        "cep": "01000-000",
        "pais": "Brasil",
        "telefone": "(11) 99999-9999"
    }]), 200

@app.route('/turmas', methods=['POST'])
@swag_from({
    'tags': ['Turmas'],
    'description': 'Cria uma nova turma.',
    'parameters': [{
        'name': 'body',
        'in': 'body',
        'required': True,
        'schema': {
            'type': 'object',
            'properties': {
                'nome_turma': {'type': 'string'},
                'id_professor': {'type': 'integer'},
                'horario': {'type': 'string'}
            },
            'example': {
                'nome_turma': 'Turma A',
                'id_professor': 1,
                'horario': '08:00 - 10:00'
            }
        }
    }],
    'responses': {
        201: {'description': 'Turma criada com sucesso'},
        400: {'description': 'Erro na requisição'}
    }
})
def create_turma():
    return jsonify({"message": "Turma criada com sucesso"}), 201

@app.route('/turmas/<int:id_turma>', methods=['GET'])
@swag_from({
    'tags': ['Turmas'],
    'description': 'Busca os dados de uma turma pelo ID.',
    'parameters': [{
        'name': 'id_turma',
        'in': 'path',
        'required': True,
        'type': 'integer'
    }],
    'responses': {
        200: {'description': 'Dados da turma'},
        404: {'description': 'Turma não encontrada'}
    }
})
def read_turma(id_turma):
    return jsonify({"id_turma": id_turma, "nome_turma": "Turma A", "id_professor": 1, "horario": "08:00 - 10:00"}), 200

@app.route('/turmas', methods=['GET'])
@swag_from({
    'tags': ['Turmas'],
    'description': 'Lista todas as turmas cadastradas.',
    'responses': {
        200: {'description': 'Lista de turmas'}
    }
})
def read_all_turmas():
    return jsonify([]), 200

@app.route('/turmas/<int:id_turma>', methods=['PUT'])
@swag_from({
    'tags': ['Turmas'],
    'description': 'Atualiza os dados de uma turma.',
    'parameters': [
        {
            'name': 'id_turma',
            'in': 'path',
            'required': True,
            'type': 'integer'
        },
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'nome_turma': {'type': 'string'},
                    'id_professor': {'type': 'integer'},
                    'horario': {'type': 'string'}
                },
                'example': {
                    'nome_turma': 'Turma B',
                    'id_professor': 2,
                    'horario': '10:00 - 12:00'
                }
            }
        }
    ],
    'responses': {
        200: {'description': 'Turma atualizada com sucesso'},
        404: {'description': 'Turma não encontrada'},
        400: {'description': 'Erro na requisição'}
    }
})
def update_turma(id_turma):
    return jsonify({"message": "Turma atualizada com sucesso"}), 200

@app.route('/turmas/<int:id_turma>', methods=['DELETE'])
@swag_from({
    'tags': ['Turmas'],
    'description': 'Deleta uma turma pelo ID.',
    'parameters': [{
        'name': 'id_turma',
        'in': 'path',
        'required': True,
        'type': 'integer'
    }],
    'responses': {
        200: {'description': 'Turma deletada com sucesso'},
        404: {'description': 'Turma não encontrada'},
        400: {'description': 'Erro na requisição'}
    }
})
def delete_turma(id_turma):
    return jsonify({"message": "Turma deletada com sucesso"}), 200

@app.route('/professores', methods=['POST'])
@swag_from({
    'tags': ['Professores'],
    'description': 'Cria um novo professor.',
    'parameters': [{
        'name': 'body',
        'in': 'body',
        'required': True,
        'schema': {
            'type': 'object',
            'properties': {
                'professor_id': {'type': 'string'},
                'nome': {'type': 'string'},
                'especialidade': {'type': 'string'}
            },
            'example': {
                'professor_id': 'P001',
                'nome': 'Maria Souza',
                'especialidade': 'Matemática'
            }
        }
    }],
    'responses': {
        201: {'description': 'Professor criado com sucesso'},
        400: {'description': 'Erro na requisição'}
    }
})
def create_professor():
    return jsonify({"message": "Professor criado com sucesso"}), 201

@app.route('/pagamentos', methods=['POST'])
@swag_from({
    'tags': ['Pagamentos'],
    'description': 'Registra um novo pagamento.',
    'parameters': [{
        'name': 'body',
        'in': 'body',
        'required': True,
        'schema': {
            'type': 'object',
            'properties': {
                'pagamento_id': {'type': 'string'},
                'aluno_id': {'type': 'string'},
                'valor': {'type': 'number'},
                'data': {'type': 'string', 'format': 'date'}
            },
            'example': {
                'pagamento_id': 'PG001',
                'aluno_id': '123',
                'valor': 500.0,
                'data': '2025-04-29'
            }
        }
    }],
    'responses': {
        201: {'description': 'Pagamento registrado com sucesso'},
        400: {'description': 'Erro na requisição'}
    }
})
def create_pagamento():
    return jsonify({"message": "Pagamento registrado com sucesso"}), 201

@app.route('/')
def docs_redirect():
    return jsonify({"message": "Acesse a documentação em /apidocs/"}), 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)