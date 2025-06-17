from flask import Blueprint, request, jsonify
from .Utils.bd import create_connection
from flasgger import swag_from

app = Blueprint('turmas', __name__)

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
            'required': ['nome_turma'],
            'example': {
                'nome_turma': 'Turma A',
                'id_professor': 1,
                'horario': '08:00 - 10:00'
            }
        }
    }],
    'responses': {
        201: {
            'description': 'Turma criada com sucesso',
            'schema': {
                'type': 'object',
                'properties': {
                    'message': {'type': 'string'},
                    'id_turma': {'type': 'integer'}
                }
            }
        },
        400: {'description': 'Erro na requisição'},
        500: {'description': 'Erro no servidor'}
    }
})
def create_turma():
    data = request.get_json()
    
    # Validação de dados
    if not data or 'nome_turma' not in data:
        return jsonify({"error": "Nome da turma é obrigatório"}), 400
        
    conn = create_connection()
    if not conn:
        return jsonify({"error": "Falha na conexão com o banco de dados"}), 500
        
    cursor = conn.cursor()
    try:
        # Verificar se o professor existe, caso tenha sido informado
        if 'id_professor' in data and data['id_professor']:
            cursor.execute("SELECT COUNT(*) FROM professor WHERE id_professor = %s", (data['id_professor'],))
            if cursor.fetchone()[0] == 0:
                return jsonify({"error": "Professor não encontrado"}), 400
        
        cursor.execute(
            """
            INSERT INTO turma (nome_turma, id_professor, horario)
            VALUES (%s, %s, %s)
            """,
            (data['nome_turma'], data.get('id_professor'), data.get('horario'))
        )
        conn.commit()
        # Obter o ID gerado
        cursor.execute("SELECT LAST_INSERT_ID()")
        id_turma = cursor.fetchone()[0]
        return jsonify({"message": "Turma criada com sucesso", "id_turma": id_turma}), 201
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()
        conn.close()

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
        200: {
            'description': 'Dados da turma',
            'schema': {
                'type': 'object',
                'properties': {
                    'id_turma': {'type': 'integer'},
                    'nome_turma': {'type': 'string'},
                    'id_professor': {'type': 'integer'},
                    'horario': {'type': 'string'},
                    'nome_professor': {'type': 'string'}
                }
            }
        },
        404: {'description': 'Turma não encontrada'},
        500: {'description': 'Erro no servidor'}
    }
})
def read_turma(id_turma):
    conn = create_connection()
    if not conn:
        return jsonify({"error": "Falha na conexão com o banco de dados"}), 500
        
    cursor = conn.cursor()
    try:
        cursor.execute("""
            SELECT t.id_turma, t.nome_turma, t.id_professor, t.horario, p.nome_completo as nome_professor
            FROM turma t
            LEFT JOIN professor p ON t.id_professor = p.id_professor
            WHERE t.id_turma = %s
        """, (id_turma,))
        turma = cursor.fetchone()
        if turma is None:
            return jsonify({"error": "Turma não encontrada"}), 404
        return jsonify({
            "id_turma": turma[0],
            "nome_turma": turma[1],
            "id_professor": turma[2],
            "horario": turma[3],
            "nome_professor": turma[4]
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()
        conn.close()

@app.route('/turmas', methods=['GET'])
@swag_from({
    'tags': ['Turmas'],
    'description': 'Lista todas as turmas cadastradas.',
    'responses': {
        200: {
            'description': 'Lista de turmas',
            'schema': {
                'type': 'array',
                'items': {
                    'type': 'object',
                    'properties': {
                        'id_turma': {'type': 'integer'},
                        'nome_turma': {'type': 'string'},
                        'id_professor': {'type': 'integer'},
                        'horario': {'type': 'string'},
                        'nome_professor': {'type': 'string'}
                    }
                }
            }
        },
        500: {'description': 'Erro no servidor'}
    }
})
def read_all_turmas():
    conn = create_connection()
    if not conn:
        return jsonify({"error": "Falha na conexão com o banco de dados"}), 500
        
    cursor = conn.cursor()
    try:
        cursor.execute("""
            SELECT t.id_turma, t.nome_turma, t.id_professor, t.horario, p.nome_completo as nome_professor
            FROM turma t
            LEFT JOIN professor p ON t.id_professor = p.id_professor
            ORDER BY t.nome_turma
        """)
        turmas = cursor.fetchall()
        
        result = []
        for turma in turmas:
            result.append({
                "id_turma": turma[0],
                "nome_turma": turma[1],
                "id_professor": turma[2],
                "horario": turma[3],
                "nome_professor": turma[4]
            })
        
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()
        conn.close()

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
                'required': ['nome_turma'],
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
        400: {'description': 'Erro na requisição'},
        404: {'description': 'Turma não encontrada'},
        500: {'description': 'Erro no servidor'}
    }
})
def update_turma(id_turma):
    data = request.get_json()
    
    # Validação de dados
    if not data or 'nome_turma' not in data:
        return jsonify({"error": "Nome da turma é obrigatório"}), 400
        
    conn = create_connection()
    if not conn:
        return jsonify({"error": "Falha na conexão com o banco de dados"}), 500
        
    cursor = conn.cursor()
    try:
        # Verificar se a turma existe
        cursor.execute("SELECT COUNT(*) FROM turma WHERE id_turma = %s", (id_turma,))
        if cursor.fetchone()[0] == 0:
            return jsonify({"error": "Turma não encontrada"}), 404
            
        # Verificar se o professor existe, caso tenha sido informado
        if 'id_professor' in data and data['id_professor']:
            cursor.execute("SELECT COUNT(*) FROM professor WHERE id_professor = %s", (data['id_professor'],))
            if cursor.fetchone()[0] == 0:
                return jsonify({"error": "Professor não encontrado"}), 400
                
        cursor.execute(
            """
            UPDATE turma
            SET nome_turma = %s, id_professor = %s, horario = %s
            WHERE id_turma = %s
            """,
            (data['nome_turma'], data.get('id_professor'), data.get('horario'), id_turma)
        )
        conn.commit()
        return jsonify({"message": "Turma atualizada com sucesso"}), 200
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()
        conn.close()

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
        400: {'description': 'Erro na requisição ou turma possui alunos associados'},
        404: {'description': 'Turma não encontrada'},
        500: {'description': 'Erro no servidor'}
    }
})
def delete_turma(id_turma):
    conn = create_connection()
    if not conn:
        return jsonify({"error": "Falha na conexão com o banco de dados"}), 500
        
    cursor = conn.cursor()
    try:
        # Verificar se há alunos associados à turma
        cursor.execute("SELECT COUNT(*) FROM aluno WHERE id_turma = %s", (id_turma,))
        if cursor.fetchone()[0] > 0:
            return jsonify({"error": "Não é possível excluir a turma pois possui alunos associados"}), 400
            
        cursor.execute("DELETE FROM turma WHERE id_turma = %s", (id_turma,))
        conn.commit()
        if cursor.rowcount == 0:
            return jsonify({"error": "Turma não encontrada"}), 404
        return jsonify({"message": "Turma deletada com sucesso"}), 200
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()
        conn.close()