from flask import Blueprint, request, jsonify
from .Utils.bd import create_connection
import datetime
from flasgger import swag_from

app = Blueprint('presencas', __name__)

@app.route('/presencas', methods=['POST'])
@swag_from({
    'tags': ['Presencas'],
    'description': 'Registra uma nova presença.',
    'parameters': [{
        'name': 'body',
        'in': 'body',
        'required': True,
        'schema': {
            'type': 'object',
            'properties': {
                'id_aluno': {'type': 'integer'},
                'data_presenca': {'type': 'string', 'format': 'date'},
                'presente': {'type': 'boolean'}
            },
            'required': ['id_aluno', 'data_presenca', 'presente'],
            'example': {
                'id_aluno': 0,
                'data_presenca': '',
                'presente': False
            }
        }
    }],
    'responses': {
        201: {'description': 'Presença registrada com sucesso'},
        400: {'description': 'Erro na requisição'},
        404: {'description': 'Aluno não encontrado'},
        500: {'description': 'Erro no servidor'}
    }
})
def create_presenca():
    data = request.get_json()
    
    # Validação dos dados de entrada
    if not data or 'id_aluno' not in data or 'data_presenca' not in data or 'presente' not in data:
        return jsonify({"error": "Os campos id_aluno, data_presenca e presente são obrigatórios"}), 400
    
    conn = create_connection()
    if not conn:
        return jsonify({"error": "Não foi possível conectar ao banco de dados"}), 500
        
    cursor = conn.cursor()
    try:
        # Verificar se o aluno existe
        cursor.execute("SELECT COUNT(*) FROM aluno WHERE id_aluno = %s", (data['id_aluno'],))
        if cursor.fetchone()[0] == 0:
            return jsonify({"error": "Aluno não encontrado"}), 404
            
        # Verificar se já existe uma presença para este aluno nesta data
        cursor.execute(
            "SELECT COUNT(*) FROM presenca WHERE id_aluno = %s AND data_presenca = %s",
            (data['id_aluno'], data['data_presenca'])
        )
        if cursor.fetchone()[0] > 0:
            return jsonify({"error": "Já existe um registro de presença para este aluno nesta data"}), 400
            
        cursor.execute(
            """
            INSERT INTO presenca (id_aluno, data_presenca, presente)
            VALUES (%s, %s, %s)
            RETURNING id_presenca
            """,
            (data['id_aluno'], data['data_presenca'], data['presente'])
        )
        id_presenca = cursor.fetchone()[0]
        conn.commit()
        return jsonify({"message": "Presença registrada com sucesso", "id_presenca": id_presenca}), 201
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()
        conn.close()

@app.route('/presencas/<int:id_presenca>', methods=['GET'])
@swag_from({
    'tags': ['Presencas'],
    'description': 'Busca uma presença pelo ID.',
    'parameters': [{
        'name': 'id_presenca',
        'in': 'path',
        'required': True,
        'type': 'integer'
    }],
    'responses': {
        200: {
            'description': 'Dados da presença',
            'schema': {
                'type': 'object',
                'properties': {
                    'id_presenca': {'type': 'integer'},
                    'id_aluno': {'type': 'integer'},
                    'data_presenca': {'type': 'string', 'format': 'date'},
                    'presente': {'type': 'boolean'}
                }
            }
        },
        404: {'description': 'Presença não encontrada'},
        500: {'description': 'Erro no servidor'}
    }
})
def read_presenca(id_presenca):
    conn = create_connection()
    if not conn:
        return jsonify({"error": "Não foi possível conectar ao banco de dados"}), 500
        
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM presenca WHERE id_presenca = %s", (id_presenca,))
        presenca = cursor.fetchone()
        if presenca is None:
            return jsonify({"error": "Presença não encontrada"}), 404
            
        # Convertendo objetos datetime para strings
        data_presenca = presenca[2]
        if isinstance(data_presenca, datetime.datetime):
            data_presenca = data_presenca.strftime('%Y-%m-%d')
            
        return jsonify({
            "id_presenca": presenca[0],
            "id_aluno": presenca[1],
            "data_presenca": data_presenca,
            "presente": bool(presenca[3])  # Convertendo para booleano
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()
        conn.close()

@app.route('/presencas', methods=['GET'])
@swag_from({
    'tags': ['Presencas'],
    'description': 'Lista todas as presenças com opções de filtro.',
    'parameters': [
        {
            'name': 'id_aluno',
            'in': 'query',
            'type': 'integer',
            'required': False,
            'description': 'Filtrar por ID do aluno'
        },
        {
            'name': 'data_inicio',
            'in': 'query',
            'type': 'string',
            'format': 'date',
            'required': False,
            'description': 'Data inicial para filtro'
        },
        {
            'name': 'data_fim',
            'in': 'query',
            'type': 'string',
            'format': 'date',
            'required': False,
            'description': 'Data final para filtro'
        },
        {
            'name': 'presente',
            'in': 'query',
            'type': 'boolean',
            'required': False,
            'description': 'Filtrar por status de presença'
        }
    ],
    'responses': {
        200: {
            'description': 'Lista de presenças',
            'schema': {
                'type': 'array',
                'items': {
                    'type': 'object',
                    'properties': {
                        'id_presenca': {'type': 'integer'},
                        'id_aluno': {'type': 'integer'},
                        'data_presenca': {'type': 'string', 'format': 'date'},
                        'presente': {'type': 'boolean'}
                    }
                }
            }
        },
        500: {'description': 'Erro no servidor'}
    }
})
def read_all_presencas():
    conn = create_connection()
    if not conn:
        return jsonify({"error": "Não foi possível conectar ao banco de dados"}), 500
        
    cursor = conn.cursor()
    try:
        # Adicionando parâmetros de filtro opcionais
        filtros = []
        valores = []
        
        id_aluno = request.args.get('id_aluno')
        if id_aluno:
            filtros.append("id_aluno = %s")
            valores.append(id_aluno)
            
        data_inicio = request.args.get('data_inicio')
        if data_inicio:
            filtros.append("data_presenca >= %s")
            valores.append(data_inicio)
            
        data_fim = request.args.get('data_fim')
        if data_fim:
            filtros.append("data_presenca <= %s")
            valores.append(data_fim)
            
        presente = request.args.get('presente')
        if presente is not None:
            filtros.append("presente = %s")
            valores.append(presente.lower() == 'true')
        
        # Construir a consulta com os filtros
        query = "SELECT * FROM presenca"
        if filtros:
            query += " WHERE " + " AND ".join(filtros)
        query += " ORDER BY data_presenca DESC"
        
        cursor.execute(query, tuple(valores))
        presencas = cursor.fetchall()
        
        result = []
        for presenca in presencas:
            # Convertendo objetos datetime para strings
            data_presenca = presenca[2]
            if isinstance(data_presenca, datetime.datetime):
                data_presenca = data_presenca.strftime('%Y-%m-%d')
                
            result.append({
                "id_presenca": presenca[0],
                "id_aluno": presenca[1],
                "data_presenca": data_presenca,
                "presente": bool(presenca[3])  # Convertendo para booleano
            })
        
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()
        conn.close()

@app.route('/presencas/<int:id_presenca>', methods=['PUT'])
@swag_from({
    'tags': ['Presencas'],
    'description': 'Atualiza os dados de uma presença.',
    'parameters': [
        {
            'name': 'id_presenca',
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
                    'id_aluno': {'type': 'integer'},
                    'data_presenca': {'type': 'string', 'format': 'date'},
                    'presente': {'type': 'boolean'}
                },
                'example': {
                    'id_aluno': 0,
                    'data_presenca': '',
                    'presente': False
                }
            }
        }
    ],
    'responses': {
        200: {'description': 'Presença atualizada com sucesso'},
        400: {'description': 'Erro na requisição'},
        404: {'description': 'Presença ou aluno não encontrado'},
        500: {'description': 'Erro no servidor'}
    }
})
def update_presenca(id_presenca):
    data = request.get_json()
    
    # Validação dos dados de entrada
    if not data:
        return jsonify({"error": "Dados inválidos"}), 400
        
    conn = create_connection()
    if not conn:
        return jsonify({"error": "Não foi possível conectar ao banco de dados"}), 500
        
    cursor = conn.cursor()
    try:
        # Verificar se a presença existe
        cursor.execute("SELECT * FROM presenca WHERE id_presenca = %s", (id_presenca,))
        presenca_atual = cursor.fetchone()
        if presenca_atual is None:
            return jsonify({"error": "Presença não encontrada"}), 404
            
        # Verificar se o aluno existe, se estiver sendo atualizado
        if 'id_aluno' in data:
            cursor.execute("SELECT COUNT(*) FROM aluno WHERE id_aluno = %s", (data['id_aluno'],))
            if cursor.fetchone()[0] == 0:
                return jsonify({"error": "Aluno não encontrado"}), 404
                
        # Verificar se já existe uma presença para este aluno nesta data (evitar duplicidade)
        if 'id_aluno' in data or 'data_presenca' in data:
            id_aluno = data.get('id_aluno', presenca_atual[1])
            data_presenca = data.get('data_presenca', presenca_atual[2])
            
            cursor.execute(
                """
                SELECT COUNT(*) FROM presenca 
                WHERE id_aluno = %s 
                AND data_presenca = %s 
                AND id_presenca != %s
                """,
                (id_aluno, data_presenca, id_presenca)
            )
            if cursor.fetchone()[0] > 0:
                return jsonify({"error": "Já existe um registro de presença para este aluno nesta data"}), 400
        
        cursor.execute(
            """
            UPDATE presenca
            SET id_aluno = %s, data_presenca = %s, presente = %s
            WHERE id_presenca = %s
            """,
            (
                data.get('id_aluno', presenca_atual[1]),
                data.get('data_presenca', presenca_atual[2]),
                data.get('presente', presenca_atual[3]),
                id_presenca
            )
        )
        conn.commit()
        return jsonify({"message": "Presença atualizada com sucesso"}), 200
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()
        conn.close()

@app.route('/presencas/<int:id_presenca>', methods=['DELETE'])
@swag_from({
    'tags': ['Presencas'],
    'description': 'Deleta uma presença pelo ID.',
    'parameters': [{
        'name': 'id_presenca',
        'in': 'path',
        'required': True,
        'type': 'integer'
    }],
    'responses': {
        200: {'description': 'Presença deletada com sucesso'},
        404: {'description': 'Presença não encontrada'},
        500: {'description': 'Erro no servidor'}
    }
})
def delete_presenca(id_presenca):
    conn = create_connection()
    if not conn:
        return jsonify({"error": "Não foi possível conectar ao banco de dados"}), 500
        
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM presenca WHERE id_presenca = %s", (id_presenca,))
        conn.commit()
        if cursor.rowcount == 0:
            return jsonify({"error": "Presença não encontrada"}), 404
        return jsonify({"message": "Presença deletada com sucesso"}), 200
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()
        conn.close()