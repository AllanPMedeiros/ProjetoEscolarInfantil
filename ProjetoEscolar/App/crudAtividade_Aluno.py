from flask import Blueprint, request, jsonify
from .Utils.bd import create_connection
from flasgger import swag_from

app = Blueprint('atividades_alunos', __name__)

# CRUD para Atividade_Aluno
@app.route('/atividades_alunos', methods=['POST'])
@swag_from({
    'tags': ['Atividades_Alunos'],
    'description': 'Associa uma atividade a um aluno.',
    'parameters': [{
        'name': 'body',
        'in': 'body',
        'required': True,
        'schema': {
            'type': 'object',
            'properties': {
                'id_atividade': {'type': 'integer'},
                'id_aluno': {'type': 'integer'}
            },
            'required': ['id_atividade', 'id_aluno'],
            'example': {
                'id_atividade': 1,
                'id_aluno': 1
            }
        }
    }],
    'responses': {
        201: {'description': 'Atividade-Aluno criada com sucesso'},
        400: {'description': 'Erro na requisição'},
        500: {'description': 'Erro no servidor'}
    }
})
def create_atividade_aluno():
    data = request.get_json()
    
    # Validação dos dados de entrada
    if not data or 'id_atividade' not in data or 'id_aluno' not in data:
        return jsonify({"error": "Dados incompletos. id_atividade e id_aluno são obrigatórios"}), 400
        
    conn = create_connection()
    if not conn:
        return jsonify({"error": "Falha na conexão com o banco de dados"}), 500
        
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            INSERT INTO atividade_aluno (id_atividade, id_aluno)
            VALUES (%s, %s)
            """,
            (data['id_atividade'], data['id_aluno'])
        )
        conn.commit()
        return jsonify({"message": "Atividade-Aluno criada com sucesso"}), 201
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()
        conn.close()

@app.route('/atividades_alunos/<int:id_atividade>/<int:id_aluno>', methods=['GET'])
@swag_from({
    'tags': ['Atividades_Alunos'],
    'description': 'Busca uma associação entre atividade e aluno pelos IDs.',
    'parameters': [
        {
            'name': 'id_atividade',
            'in': 'path',
            'required': True,
            'type': 'integer'
        },
        {
            'name': 'id_aluno',
            'in': 'path',
            'required': True,
            'type': 'integer'
        }
    ],
    'responses': {
        200: {
            'description': 'Dados da associação atividade-aluno',
            'schema': {
                'type': 'object',
                'properties': {
                    'id_atividade': {'type': 'integer'},
                    'id_aluno': {'type': 'integer'}
                }
            }
        },
        404: {'description': 'Atividade-Aluno não encontrada'},
        500: {'description': 'Erro no servidor'}
    }
})
def read_atividade_aluno(id_atividade, id_aluno):
    conn = create_connection()
    if not conn:
        return jsonify({"error": "Falha na conexão com o banco de dados"}), 500
        
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM atividade_aluno WHERE id_atividade = %s AND id_aluno = %s", (id_atividade, id_aluno))
        atividade_aluno = cursor.fetchone()
        if atividade_aluno is None:
            return jsonify({"error": "Atividade-Aluno não encontrada"}), 404
        return jsonify({
            "id_atividade": atividade_aluno[0],
            "id_aluno": atividade_aluno[1]
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()
        conn.close()

@app.route('/atividades_alunos', methods=['GET'])
@swag_from({
    'tags': ['Atividades_Alunos'],
    'description': 'Lista todas as associações entre atividades e alunos.',
    'responses': {
        200: {
            'description': 'Lista de associações atividade-aluno',
            'schema': {
                'type': 'array',
                'items': {
                    'type': 'object',
                    'properties': {
                        'id_atividade': {'type': 'integer'},
                        'id_aluno': {'type': 'integer'}
                    }
                }
            }
        },
        500: {'description': 'Erro no servidor'}
    }
})
def read_all_atividades_alunos():
    conn = create_connection()
    if not conn:
        return jsonify({"error": "Falha na conexão com o banco de dados"}), 500
        
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM atividade_aluno")
        atividades_alunos = cursor.fetchall()
        
        result = []
        for atividade_aluno in atividades_alunos:
            result.append({
                "id_atividade": atividade_aluno[0],
                "id_aluno": atividade_aluno[1]
            })
        
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()
        conn.close()

@app.route('/atividades_alunos/<int:id_atividade>/<int:id_aluno>', methods=['DELETE'])
@swag_from({
    'tags': ['Atividades_Alunos'],
    'description': 'Remove uma associação entre atividade e aluno pelos IDs.',
    'parameters': [
        {
            'name': 'id_atividade',
            'in': 'path',
            'required': True,
            'type': 'integer'
        },
        {
            'name': 'id_aluno',
            'in': 'path',
            'required': True,
            'type': 'integer'
        }
    ],
    'responses': {
        200: {'description': 'Atividade-Aluno deletada com sucesso'},
        404: {'description': 'Atividade-Aluno não encontrada'},
        500: {'description': 'Erro no servidor'}
    }
})
def delete_atividade_aluno(id_atividade, id_aluno):
    conn = create_connection()
    if not conn:
        return jsonify({"error": "Falha na conexão com o banco de dados"}), 500
        
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM atividade_aluno WHERE id_atividade = %s AND id_aluno = %s", (id_atividade, id_aluno))
        conn.commit()
        if cursor.rowcount == 0:
            return jsonify({"error": "Atividade-Aluno não encontrada"}), 404
        return jsonify({"message": "Atividade-Aluno deletada com sucesso"}), 200
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()
        conn.close()