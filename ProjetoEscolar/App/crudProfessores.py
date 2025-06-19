from flask import Blueprint, request, jsonify
from .Utils.bd import create_connection
from flasgger import swag_from

# Blueprint para rotas de professores
app = Blueprint('professores', __name__)

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
                'id_professor': {'type': 'integer'},
                'nome_completo': {'type': 'string'},
                'email': {'type': 'string'},
                'telefone': {'type': 'string'}
            },
            'required': ['nome_completo'],
            'example': {
                'nome_completo': 'Maria Souza',
                'email': 'maria.souza@email.com',
                'telefone': '(11) 98765-4321'
            }
        }
    }],
    'responses': {
        201: {'description': 'Professor criado com sucesso'},
        400: {'description': 'Erro na requisição'},
        500: {'description': 'Erro no servidor'}
    }
})
def create_professor():
    data = request.get_json()
    conn = create_connection()
    if conn is None:
        return jsonify({"error": "Falha na conexão com o banco de dados"}), 500
    
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            INSERT INTO professor (nome_completo, email, telefone)
            VALUES (%s, %s, %s)
            """,
            (data['nome_completo'], data.get('email'), data.get('telefone'))
        )
        conn.commit()
        return jsonify({"message": "Professor criado com sucesso"}), 201
    except Exception as e:
        conn.rollback()
        print(f"Erro ao criar professor: {str(e)}")
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()
        conn.close()

@app.route('/professores/<int:id_professor>', methods=['GET'])
@swag_from({
    'tags': ['Professores'],
    'description': 'Busca um professor pelo ID.',
    'parameters': [{
        'name': 'id_professor',
        'in': 'path',
        'required': True,
        'type': 'integer'
    }],
    'responses': {
        200: {
            'description': 'Dados do professor',
            'schema': {
                'type': 'object',
                'properties': {
                    'id_professor': {'type': 'integer'},
                    'nome_completo': {'type': 'string'},
                    'email': {'type': 'string'},
                    'telefone': {'type': 'string'}
                }
            }
        },
        404: {'description': 'Professor não encontrado'},
        500: {'description': 'Erro no servidor'}
    }
})
def read_professor(id_professor):
    conn = create_connection()
    if conn is None:
        return jsonify({"error": "Falha na conexão com o banco de dados"}), 500
    
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM professor WHERE id_professor = %s", (id_professor,))
        professor = cursor.fetchone()
        if professor is None:
            return jsonify({"error": "Professor não encontrado"}), 404
        return jsonify({
            "id_professor": professor[0],
            "nome_completo": professor[1],
            "email": professor[2],
            "telefone": professor[3]
        }), 200
    except Exception as e:
        print(f"Erro ao buscar professor: {str(e)}")
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()
        conn.close()

@app.route('/professores', methods=['GET'])
@swag_from({
    'tags': ['Professores'],
    'description': 'Lista todos os professores cadastrados.',
    'responses': {
        200: {
            'description': 'Lista de professores',
            'schema': {
                'type': 'array',
                'items': {
                    'type': 'object',
                    'properties': {
                        'id_professor': {'type': 'integer'},
                        'nome_completo': {'type': 'string'},
                        'email': {'type': 'string'},
                        'telefone': {'type': 'string'}
                    }
                }
            }
        },
        500: {'description': 'Erro no servidor'}
    }
})
def read_all_professores():
    conn = create_connection()
    if conn is None:
        return jsonify({"error": "Falha na conexão com o banco de dados"}), 500
    
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM professor ORDER BY nome_completo")
        professores = cursor.fetchall()
        
        result = []
        for professor in professores:
            result.append({
                "id_professor": professor[0],
                "nome_completo": professor[1],
                "email": professor[2],
                "telefone": professor[3]
            })
        
        return jsonify(result), 200
    except Exception as e:
        print(f"Erro ao listar professores: {str(e)}")
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()
        conn.close()

@app.route('/professores/<int:id_professor>', methods=['PUT'])
@swag_from({
    'tags': ['Professores'],
    'description': 'Atualiza os dados de um professor.',
    'parameters': [
        {
            'name': 'id_professor',
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
                    'nome_completo': {'type': 'string'},
                    'email': {'type': 'string'},
                    'telefone': {'type': 'string'}
                },
                'required': ['nome_completo'],
                'example': {
                    'nome_completo': 'Maria Souza Silva',
                    'email': 'maria.silva@email.com',
                    'telefone': '(11) 98765-4321'
                }
            }
        }
    ],
    'responses': {
        200: {'description': 'Professor atualizado com sucesso'},
        400: {'description': 'Erro na requisição'},
        404: {'description': 'Professor não encontrado'},
        500: {'description': 'Erro no servidor'}
    }
})
def update_professor(id_professor):
    data = request.get_json()
    conn = create_connection()
    if conn is None:
        return jsonify({"error": "Falha na conexão com o banco de dados"}), 500
    
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            UPDATE professor
            SET nome_completo = %s, email = %s, telefone = %s
            WHERE id_professor = %s
            """,
            (data['nome_completo'], data.get('email'), data.get('telefone'), id_professor)
        )
        conn.commit()
        if cursor.rowcount == 0:
            return jsonify({"error": "Professor não encontrado"}), 404
        return jsonify({"message": "Professor atualizado com sucesso"}), 200
    except Exception as e:
        conn.rollback()
        print(f"Erro ao atualizar professor: {str(e)}")
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()
        conn.close()

@app.route('/professores/<int:id_professor>', methods=['DELETE'])
@swag_from({
    'tags': ['Professores'],
    'description': 'Deleta um professor pelo ID.',
    'parameters': [{
        'name': 'id_professor',
        'in': 'path',
        'required': True,
        'type': 'integer'
    }],
    'responses': {
        200: {'description': 'Professor deletado com sucesso'},
        400: {'description': 'Erro na requisição'},
        404: {'description': 'Professor não encontrado'},
        500: {'description': 'Erro no servidor'}
    }
})
def delete_professor(id_professor):
    conn = create_connection()
    if conn is None:
        return jsonify({"error": "Falha na conexão com o banco de dados"}), 500
    
    cursor = conn.cursor()
    try:
        # Verificar se o professor existe
        cursor.execute("SELECT COUNT(*) FROM professor WHERE id_professor = %s", (id_professor,))
        if cursor.fetchone()[0] == 0:
            return jsonify({"error": "Professor não encontrado"}), 404
            
        # Atualizar turmas para remover a referência ao professor
        cursor.execute("UPDATE turma SET id_professor = NULL WHERE id_professor = %s", (id_professor,))
        
        # Atualizar usuários para remover a referência ao professor
        cursor.execute("UPDATE usuario SET id_professor = NULL WHERE id_professor = %s", (id_professor,))
        
        # Excluir o professor
        cursor.execute("DELETE FROM professor WHERE id_professor = %s", (id_professor,))
        conn.commit()
        return jsonify({"message": "Professor deletado com sucesso"}), 200
    except Exception as e:
        conn.rollback()
        print(f"Erro ao deletar professor: {str(e)}")
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()
        conn.close()