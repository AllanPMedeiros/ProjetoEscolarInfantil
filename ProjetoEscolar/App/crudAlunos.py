from flask import Blueprint, request, jsonify
from .Utils.bd import create_connection
from flasgger import swag_from

app = Blueprint('crud_alunos_app', __name__)

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
                'nome_completo': {'type': 'string'},
                'data_nascimento': {'type': 'string', 'format': 'date'},
                'id_turma': {'type': 'integer'},
                'nome_responsavel': {'type': 'string'},
                'telefone_responsavel': {'type': 'string'},
                'email_responsavel': {'type': 'string'},
                'informacoes_adicionais': {'type': 'text'}
            },
            'required': ['nome_completo', 'data_nascimento'],
            'example': {
                'nome_completo': '',
                'data_nascimento': '',
                'id_turma': 0,
                'nome_responsavel': '',
                'telefone_responsavel': '',
                'email_responsavel': '',
                'informacoes_adicionais': ''
            }
        }
    }],
    'responses': {
        201: {'description': 'Aluno criado com sucesso'},
        400: {'description': 'Erro na requisição'},
        500: {'description': 'Erro no servidor'}
    }
})
def create_aluno():
    data = request.get_json()
    
    # Validação dos dados de entrada
    if not data or 'nome_completo' not in data:
        return jsonify({"error": "O campo nome_completo é obrigatório"}), 400
    
    conn = create_connection()
    if not conn:
        return jsonify({"error": "Não foi possível conectar ao banco de dados"}), 500
        
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            INSERT INTO aluno (nome_completo, data_nascimento, id_turma, nome_responsavel, telefone_responsavel, email_responsavel, informacoes_adicionais)
            VALUES (%s,%s,%s,%s,%s,%s,%s)
            RETURNING id_aluno
            """,
            (data['nome_completo'], data.get('data_nascimento', '2000-01-01'), 
             data.get('id_turma'), data.get('nome_responsavel'), data.get('telefone_responsavel'),
             data.get('email_responsavel'), data.get('informacoes_adicionais'))
        )
        id_aluno = cursor.fetchone()[0]
        conn.commit()
        return jsonify({"message": "Aluno criado com sucesso", "id_aluno": id_aluno}), 201
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()
        conn.close()

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
            'schema': {
                'type': 'object',
                'properties': {
                    'id_aluno': {'type': 'integer'},
                    'nome_completo': {'type': 'string'},
                    'data_nascimento': {'type': 'string', 'format': 'date'},
                    'id_turma': {'type': 'integer'},
                    'nome_responsavel': {'type': 'string'},
                    'telefone_responsavel': {'type': 'string'},
                    'email_responsavel': {'type': 'string'},
                    'informacoes_adicionais': {'type': 'string'}
                }
            }
        },
        404: {'description': 'Aluno não encontrado'},
        500: {'description': 'Erro no servidor'}
    }
})
def read_aluno(aluno_id):
    conn = create_connection()
    if not conn:
        return jsonify({"error": "Não foi possível conectar ao banco de dados"}), 500
        
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM aluno WHERE id_aluno = %s", (int(aluno_id),))
        aluno = cursor.fetchone()
        if aluno is None:
            return jsonify({"error": "Aluno não encontrado"}), 404
        
        # Convertendo objetos não serializáveis (como datetime) para string
        data_nascimento = aluno[2]
        if data_nascimento:
            data_nascimento = data_nascimento.strftime('%Y-%m-%d')
            
        result = {
            "aluno_id": aluno[0],
            "nome": aluno[1],
            "data_nascimento": data_nascimento,
            "id_turma": aluno[3],
            "nome_responsavel": aluno[4],
            "telefone_responsavel": aluno[5],
            "email_responsavel": aluno[6],
            "informacoes_adicionais": aluno[7]
        }
        
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()
        conn.close()

@app.route('/alunos', methods=['GET'])
@swag_from({
    'tags': ['Alunos'],
    'description': 'Lista todos os alunos cadastrados.',
    'responses': {
        200: {
            'description': 'Lista de alunos',
            'schema': {
                'type': 'array',
                'items': {
                    'type': 'object',
                    'properties': {
                        'id_aluno': {'type': 'integer'},
                        'nome_completo': {'type': 'string'},
                        'data_nascimento': {'type': 'string', 'format': 'date'},
                        'id_turma': {'type': 'integer'},
                        'nome_responsavel': {'type': 'string'},
                        'telefone_responsavel': {'type': 'string'},
                        'email_responsavel': {'type': 'string'},
                        'informacoes_adicionais': {'type': 'string'}
                    }
                }
            }
        },
        500: {'description': 'Erro no servidor'}
    }
})
def read_all_alunos():
    conn = create_connection()
    if not conn:
        return jsonify({"error": "Não foi possível conectar ao banco de dados"}), 500
        
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM aluno ORDER BY nome_completo")
        alunos = cursor.fetchall()
        
        result = []
        for aluno in alunos:
            # Convertendo objetos não serializáveis (como datetime) para string
            data_nascimento = aluno[2]
            if data_nascimento:
                data_nascimento = data_nascimento.strftime('%Y-%m-%d')
                
            result.append({
                "aluno_id": aluno[0],
                "nome": aluno[1],
                "data_nascimento": data_nascimento,
                "id_turma": aluno[3],
                "nome_responsavel": aluno[4],
                "telefone_responsavel": aluno[5],
                "email_responsavel": aluno[6],
                "informacoes_adicionais": aluno[7]
            })
        
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()
        conn.close()

@app.route('/alunos/<string:aluno_id>', methods=['PUT'])
@swag_from({
    'tags': ['Alunos'],
    'description': 'Atualiza os dados de um aluno.',
    'parameters': [
        {
            'name': 'aluno_id',
            'in': 'path',
            'required': True,
            'type': 'string'
        },
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'nome_completo': {'type': 'string'},
                    'data_nascimento': {'type': 'string', 'format': 'date'},
                    'id_turma': {'type': 'integer'},
                    'nome_responsavel': {'type': 'string'},
                    'telefone_responsavel': {'type': 'string'},
                    'email_responsavel': {'type': 'string'},
                    'informacoes_adicionais': {'type': 'string'}
                },
                'example': {
                    'nome_completo': '',
                    'data_nascimento': '',
                    'id_turma': 0,
                    'nome_responsavel': '',
                    'telefone_responsavel': '',
                    'email_responsavel': '',
                    'informacoes_adicionais': '',
                    'telefone_responsavel': '',
                    'email_responsavel': '',
                    'informacoes_adicionais': ''
                }
            }
        }
    ],
    'responses': {
        200: {'description': 'Aluno atualizado com sucesso'},
        400: {'description': 'Erro na requisição'},
        404: {'description': 'Aluno não encontrado'},
        500: {'description': 'Erro no servidor'}
    }
})
def update_aluno(aluno_id):
    data = request.get_json()
    
    # Validação dos dados de entrada
    if not data or 'nome_completo' not in data:
        return jsonify({"error": "O campo nome_completo é obrigatório"}), 400
    
    conn = create_connection()
    if not conn:
        return jsonify({"error": "Não foi possível conectar ao banco de dados"}), 500
        
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            UPDATE aluno
            SET nome_completo = %s, data_nascimento = %s, id_turma = %s, nome_responsavel = %s, 
                telefone_responsavel = %s, email_responsavel = %s, informacoes_adicionais = %s
            WHERE id_aluno = %s
            """,
            (data['nome_completo'], data.get('data_nascimento'), data.get('id_turma'), 
             data.get('nome_responsavel'), data.get('telefone_responsavel'), data.get('email_responsavel'),
             data.get('informacoes_adicionais'), int(aluno_id))
        )
        conn.commit()
        if cursor.rowcount == 0:
            return jsonify({"error": "Aluno não encontrado"}), 404
        return jsonify({"message": "Aluno atualizado com sucesso"}), 200
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()
        conn.close()

@app.route('/alunos/<string:aluno_id>', methods=['DELETE'])
@swag_from({
    'tags': ['Alunos'],
    'description': 'Deleta um aluno pelo ID.',
    'parameters': [{
        'name': 'aluno_id',
        'in': 'path',
        'required': True,
        'type': 'string'
    }],
    'responses': {
        200: {'description': 'Aluno deletado com sucesso'},
        400: {'description': 'Erro na requisição ou aluno possui pagamentos pendentes'},
        404: {'description': 'Aluno não encontrado'},
        500: {'description': 'Erro no servidor'}
    }
})
def delete_aluno(aluno_id):
    conn = create_connection()
    if not conn:
        return jsonify({"error": "Não foi possível conectar ao banco de dados"}), 500
        
    cursor = conn.cursor()
    try:
        # Verificar se o aluno existe
        cursor.execute("SELECT COUNT(*) FROM aluno WHERE id_aluno = %s", (int(aluno_id),))
        count = cursor.fetchone()[0]
        if count == 0:
            return jsonify({"error": "Aluno não encontrado"}), 404
            
        # Verificar se existem pagamentos pendentes
        cursor.execute("SELECT COUNT(*) FROM pagamento WHERE id_aluno = %s AND status = 'pendente'", (int(aluno_id),))
        count = cursor.fetchone()[0]
        if count > 0:
            return jsonify({"error": "Não é possível excluir este aluno pois existem pagamentos pendentes associados a ele."}), 400
            
        # Excluir registros relacionados primeiro
        cursor.execute("DELETE FROM pagamento WHERE id_aluno = %s", (int(aluno_id),))
        cursor.execute("DELETE FROM presenca WHERE id_aluno = %s", (int(aluno_id),))
        cursor.execute("DELETE FROM atividade_aluno WHERE id_aluno = %s", (int(aluno_id),))
        
        # Excluir o aluno
        cursor.execute("DELETE FROM aluno WHERE id_aluno = %s", (int(aluno_id),))
        conn.commit()
        return jsonify({"message": "Aluno deletado com sucesso"}), 200
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()
        conn.close()