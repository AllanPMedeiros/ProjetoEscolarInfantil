from flask import Blueprint, request, jsonify
from .Utils.bd import create_connection
from flasgger import swag_from
from collections import OrderedDict

app = Blueprint('atividades', __name__) 

@app.route('/atividades', methods=['POST'])
@swag_from({
    'tags': ['Atividades'],
    'description': 'Cria uma nova atividade.',
    'parameters': [{
        'name': 'body',
        'in': 'body',
        'required': True,
        'schema': {
            'type': 'object',
            'properties': OrderedDict([
                ('descricao', {'type': 'string'}),
                ('data_realizacao', {'type': 'string', 'format': 'date'})
            ]),
            'required': ['descricao', 'data_realizacao'],
            'example': OrderedDict([
                ('descricao', ''),
                ('data_realizacao', '')
            ])
        }
    }],
    'responses': {
        201: {
            'description': 'Atividade criada com sucesso',
            'schema': {
                'type': 'object',
                'properties': OrderedDict([
                    ('message', {'type': 'string'}),
                    ('id_atividade', {'type': 'integer'})
                ])
            }
        },
        400: {'description': 'Erro na requisição'},
        500: {'description': 'Erro no servidor'}
    }
})
def create_atividade():
    data = request.get_json()
    
    # Validação de dados
    if not data or 'descricao' not in data or 'data_realizacao' not in data:
        return jsonify({"error": "Dados incompletos. Descrição e data_realizacao são obrigatórios"}), 400
        
    conn = create_connection()
    if not conn:
        return jsonify({"error": "Falha na conexão com o banco de dados"}), 500
        
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            INSERT INTO atividade (descricao, data_realizacao)
            VALUES (%s, %s)
            RETURNING id_atividade
            """,
            (data['descricao'], data['data_realizacao'])
        )
        id_atividade = cursor.fetchone()[0]
        conn.commit()
        return jsonify({"message": "Atividade criada com sucesso", "id_atividade": id_atividade}), 201
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()
        conn.close()

@app.route('/atividades/<int:id_atividade>', methods=['GET'])
@swag_from({
    'tags': ['Atividades'],
    'description': 'Busca uma atividade pelo ID.',
    'parameters': [{
        'name': 'id_atividade',
        'in': 'path',
        'required': True,
        'type': 'integer'
    }],
    'responses': {
        200: {
            'description': 'Dados da atividade',
            'schema': {
                'type': 'object',
                'properties': OrderedDict([
                    ('id_atividade', {'type': 'integer'}),
                    ('descricao', {'type': 'string'}),
                    ('data_realizacao', {'type': 'string', 'format': 'date'})
                ])
            }
        },
        404: {'description': 'Atividade não encontrada'},
        500: {'description': 'Erro no servidor'}
    }
})
def read_atividade(id_atividade):
    conn = create_connection()
    if not conn:
        return jsonify({"error": "Falha na conexão com o banco de dados"}), 500
        
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM atividade WHERE id_atividade = %s", (id_atividade,))
        atividade = cursor.fetchone()
        if atividade is None:
            return jsonify({"error": "Atividade não encontrada"}), 404
        return jsonify(OrderedDict([
            ("id_atividade", atividade[0]),
            ("descricao", atividade[1]),
            ("data_realizacao", atividade[2].strftime('%Y-%m-%d') if hasattr(atividade[2], 'strftime') else atividade[2])
        ])), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()
        conn.close()

@app.route('/atividades', methods=['GET'])
@swag_from({
    'tags': ['Atividades'],
    'description': 'Lista todas as atividades cadastradas.',
    'responses': {
        200: {
            'description': 'Lista de atividades',
            'schema': {
                'type': 'array',
                'items': {
                    'type': 'object',
                    'properties': OrderedDict([
                        ('id_atividade', {'type': 'integer'}),
                        ('descricao', {'type': 'string'}),
                        ('data_realizacao', {'type': 'string', 'format': 'date'})
                    ])
                }
            }
        },
        500: {'description': 'Erro no servidor'}
    }
})
def read_all_atividades():
    conn = create_connection()
    if not conn:
        return jsonify({"error": "Falha na conexão com o banco de dados"}), 500
        
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM atividade ORDER BY data_realizacao")
        atividades = cursor.fetchall()
        
        result = []
        for atividade in atividades:
            result.append(OrderedDict([
                ("id_atividade", atividade[0]),
                ("descricao", atividade[1]),
                ("data_realizacao", atividade[2].strftime('%Y-%m-%d') if hasattr(atividade[2], 'strftime') else atividade[2])
            ]))
        
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()
        conn.close()

@app.route('/atividades/<int:id_atividade>', methods=['PUT'])
@swag_from({
    'tags': ['Atividades'],
    'description': 'Atualiza os dados de uma atividade.',
    'parameters': [
        {
            'name': 'id_atividade',
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
                'properties': OrderedDict([
                    ('descricao', {'type': 'string'}),
                    ('data_realizacao', {'type': 'string', 'format': 'date'})
                ]),
                'required': ['descricao', 'data_realizacao'],
                'example': OrderedDict([
                    ('descricao', ''),
                    ('data_realizacao', '')
                ])
            }
        }
    ],
    'responses': {
        200: {'description': 'Atividade atualizada com sucesso'},
        400: {'description': 'Erro na requisição'},
        404: {'description': 'Atividade não encontrada'},
        500: {'description': 'Erro no servidor'}
    }
})
def update_atividade(id_atividade):
    data = request.get_json()
    
    # Validação de dados
    if not data or 'descricao' not in data or 'data_realizacao' not in data:
        return jsonify({"error": "Dados incompletos. Descrição e data_realizacao são obrigatórios"}), 400
        
    conn = create_connection()
    if not conn:
        return jsonify({"error": "Falha na conexão com o banco de dados"}), 500
        
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            UPDATE atividade
            SET descricao = %s, data_realizacao = %s
            WHERE id_atividade = %s
            """,
            (data['descricao'], data['data_realizacao'], id_atividade)
        )
        conn.commit()
        if cursor.rowcount == 0:
            return jsonify({"error": "Atividade não encontrada"}), 404
        return jsonify({"message": "Atividade atualizada com sucesso"}), 200
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()
        conn.close()

@app.route('/atividades/<int:id_atividade>', methods=['DELETE'])
@swag_from({
    'tags': ['Atividades'],
    'description': 'Deleta uma atividade pelo ID.',
    'parameters': [{
        'name': 'id_atividade',
        'in': 'path',
        'required': True,
        'type': 'integer'
    }],
    'responses': {
        200: {'description': 'Atividade deletada com sucesso'},
        400: {'description': 'Erro na requisição'},
        404: {'description': 'Atividade não encontrada'},
        500: {'description': 'Erro no servidor'}
    }
})
def delete_atividade(id_atividade):
    conn = create_connection()
    if not conn:
        return jsonify({"error": "Falha na conexão com o banco de dados"}), 500
        
    cursor = conn.cursor()
    try:
        # Verificar se a atividade existe
        cursor.execute("SELECT COUNT(*) FROM atividade WHERE id_atividade = %s", (id_atividade,))
        if cursor.fetchone()[0] == 0:
            return jsonify({"error": "Atividade não encontrada"}), 404
            
        # Excluir registros relacionados primeiro
        cursor.execute("DELETE FROM atividade_aluno WHERE id_atividade = %s", (id_atividade,))
        
        # Excluir a atividade
        cursor.execute("DELETE FROM atividade WHERE id_atividade = %s", (id_atividade,))
        conn.commit()
        return jsonify({"message": "Atividade deletada com sucesso"}), 200
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()
        conn.close()