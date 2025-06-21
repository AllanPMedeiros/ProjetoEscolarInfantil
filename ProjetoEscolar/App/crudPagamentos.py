from flask import Blueprint, request, jsonify
from .Utils.bd import create_connection
import datetime
from flasgger import swag_from

app = Blueprint('pagamentos', __name__)

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
                'id_aluno': {'type': 'integer'},
                'data_pagamento': {'type': 'string', 'format': 'date'},
                'valor_pago': {'type': 'number'},
                'forma_pagamento': {'type': 'string'},
                'referencia': {'type': 'string'},
                'status': {'type': 'string'}
            },
            'required': ['id_aluno', 'data_pagamento', 'valor_pago'],
            'example': {
                'id_aluno': 0,
                'data_pagamento': '',
                'valor_pago': 0.0,
                'forma_pagamento': '',
                'referencia': '',
                'status': ''
            }
        }
    }],
    'responses': {
        201: {
            'description': 'Pagamento registrado com sucesso',
            'schema': {
                'type': 'object',
                'properties': {
                    'message': {'type': 'string'},
                    'id_pagamento': {'type': 'integer'}
                }
            }
        },
        400: {'description': 'Erro na requisição'},
        404: {'description': 'Aluno não encontrado'},
        500: {'description': 'Erro no servidor'}
    }
})
def create_pagamento():
    data = request.get_json()
    
    # Validação dos dados de entrada
    if not data or 'id_aluno' not in data or 'data_pagamento' not in data or 'valor_pago' not in data:
        return jsonify({"error": "Os campos id_aluno, data_pagamento e valor_pago são obrigatórios"}), 400
    
    conn = create_connection()
    if not conn:
        return jsonify({"error": "Não foi possível conectar ao banco de dados"}), 500
        
    cursor = conn.cursor()
    try:
        # Verificar se o aluno existe
        try:
            id_aluno = int(data['id_aluno'])
        except ValueError:
            return jsonify({"error": "O ID do aluno deve ser um número inteiro"}), 400
            
        cursor.execute("SELECT COUNT(*) FROM aluno WHERE id_aluno = %s", (id_aluno,))
        if cursor.fetchone()[0] == 0:
            return jsonify({"error": "Aluno não encontrado"}), 404
            
        cursor.execute(
            """
            INSERT INTO pagamento (id_aluno, data_pagamento, valor_pago, forma_pagamento, referencia, status)
            VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING id_pagamento
            """,
            (id_aluno, data['data_pagamento'], data['valor_pago'], 
             data.get('forma_pagamento'), data.get('referencia'), data.get('status', 'Pendente'))
        )
        id_pagamento = cursor.fetchone()[0]
        conn.commit()
        return jsonify({"message": "Pagamento criado com sucesso", "id_pagamento": id_pagamento}), 201
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()
        conn.close()

@app.route('/pagamentos/<int:id_pagamento>', methods=['GET'])
@swag_from({
    'tags': ['Pagamentos'],
    'description': 'Busca um pagamento pelo ID.',
    'parameters': [{
        'name': 'id_pagamento',
        'in': 'path',
        'required': True,
        'type': 'integer'
    }],
    'responses': {
        200: {
            'description': 'Dados do pagamento',
            'schema': {
                'type': 'object',
                'properties': {
                    'id_pagamento': {'type': 'integer'},
                    'id_aluno': {'type': 'integer'},
                    'data_pagamento': {'type': 'string', 'format': 'date'},
                    'valor_pago': {'type': 'number'},
                    'forma_pagamento': {'type': 'string'},
                    'referencia': {'type': 'string'},
                    'status': {'type': 'string'}
                }
            }
        },
        404: {'description': 'Pagamento não encontrado'},
        500: {'description': 'Erro no servidor'}
    }
})
def read_pagamento(id_pagamento):
    conn = create_connection()
    if not conn:
        return jsonify({"error": "Não foi possível conectar ao banco de dados"}), 500
        
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM pagamento WHERE id_pagamento = %s", (id_pagamento,))
        pagamento = cursor.fetchone()
        if pagamento is None:
            return jsonify({"error": "Pagamento não encontrado"}), 404
            
        # Convertendo objetos datetime para strings
        data_pagamento = pagamento[2]
        if isinstance(data_pagamento, datetime.datetime):
            data_pagamento = data_pagamento.strftime('%Y-%m-%d')
            
        return jsonify({
            "id_pagamento": pagamento[0],
            "id_aluno": pagamento[1],
            "data_pagamento": data_pagamento,
            "valor_pago": float(pagamento[3]),  # Convertendo Decimal para float para serialização JSON
            "forma_pagamento": pagamento[4],
            "referencia": pagamento[5],
            "status": pagamento[6]
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()
        conn.close()

@app.route('/pagamentos', methods=['GET'])
@swag_from({
    'tags': ['Pagamentos'],
    'description': 'Lista todos os pagamentos com opções de filtro.',
    'parameters': [
        {
            'name': 'id_aluno',
            'in': 'query',
            'type': 'integer',
            'required': False,
            'description': 'Filtrar por ID do aluno'
        },
        {
            'name': 'status',
            'in': 'query',
            'type': 'string',
            'required': False,
            'description': 'Filtrar por status do pagamento'
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
        }
    ],
    'responses': {
        200: {
            'description': 'Lista de pagamentos',
            'schema': {
                'type': 'array',
                'items': {
                    'type': 'object',
                    'properties': {
                        'id_pagamento': {'type': 'integer'},
                        'id_aluno': {'type': 'integer'},
                        'data_pagamento': {'type': 'string', 'format': 'date'},
                        'valor_pago': {'type': 'number'},
                        'forma_pagamento': {'type': 'string'},
                        'referencia': {'type': 'string'},
                        'status': {'type': 'string'}
                    }
                }
            }
        },
        500: {'description': 'Erro no servidor'}
    }
})
def read_all_pagamentos():
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
            
        status = request.args.get('status')
        if status:
            filtros.append("status = %s")
            valores.append(status)
            
        data_inicio = request.args.get('data_inicio')
        if data_inicio:
            filtros.append("data_pagamento >= %s")
            valores.append(data_inicio)
            
        data_fim = request.args.get('data_fim')
        if data_fim:
            filtros.append("data_pagamento <= %s")
            valores.append(data_fim)
        
        # Construir a consulta com os filtros
        query = "SELECT * FROM pagamento"
        if filtros:
            query += " WHERE " + " AND ".join(filtros)
        query += " ORDER BY data_pagamento DESC"
        
        cursor.execute(query, tuple(valores))
        pagamentos = cursor.fetchall()
        
        result = []
        for pagamento in pagamentos:
            # Convertendo objetos datetime para strings
            data_pagamento = pagamento[2]
            if isinstance(data_pagamento, datetime.datetime):
                data_pagamento = data_pagamento.strftime('%Y-%m-%d')
                
            result.append({
                "id_pagamento": pagamento[0],
                "id_aluno": pagamento[1],
                "data_pagamento": data_pagamento,
                "valor_pago": float(pagamento[3]),  # Convertendo Decimal para float
                "forma_pagamento": pagamento[4],
                "referencia": pagamento[5],
                "status": pagamento[6]
            })
        
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()
        conn.close()

@app.route('/pagamentos/<int:id_pagamento>', methods=['PUT'])
@swag_from({
    'tags': ['Pagamentos'],
    'description': 'Atualiza os dados de um pagamento.',
    'parameters': [
        {
            'name': 'id_pagamento',
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
                    'data_pagamento': {'type': 'string', 'format': 'date'},
                    'valor_pago': {'type': 'number'},
                    'forma_pagamento': {'type': 'string'},
                    'referencia': {'type': 'string'},
                    'status': {'type': 'string'}
                },
                'example': {
                    'id_aluno': 0,
                    'data_pagamento': '',
                    'valor_pago': 0.0,
                    'forma_pagamento': '',
                    'referencia': '',
                    'status': ''
                }
            }
        }
    ],
    'responses': {
        200: {'description': 'Pagamento atualizado com sucesso'},
        400: {'description': 'Erro na requisição'},
        404: {'description': 'Pagamento ou aluno não encontrado'},
        500: {'description': 'Erro no servidor'}
    }
})
def update_pagamento(id_pagamento):
    data = request.get_json()
    
    # Validação dos dados de entrada
    if not data:
        return jsonify({"error": "Dados inválidos"}), 400
        
    conn = create_connection()
    if not conn:
        return jsonify({"error": "Não foi possível conectar ao banco de dados"}), 500
        
    cursor = conn.cursor()
    try:
        # Verificar se o pagamento existe
        cursor.execute("SELECT * FROM pagamento WHERE id_pagamento = %s", (id_pagamento,))
        if cursor.fetchone() is None:
            return jsonify({"error": "Pagamento não encontrado"}), 404
            
        # Verificar se o aluno existe, se estiver sendo atualizado
        if 'id_aluno' in data:
            try:
                id_aluno = int(data['id_aluno'])
            except ValueError:
                return jsonify({"error": "O ID do aluno deve ser um número inteiro"}), 400
                
            cursor.execute("SELECT COUNT(*) FROM aluno WHERE id_aluno = %s", (id_aluno,))
            if cursor.fetchone()[0] == 0:
                return jsonify({"error": "Aluno não encontrado"}), 404
                
        # Obter os valores atuais
        cursor.execute("SELECT id_aluno, data_pagamento, valor_pago, forma_pagamento, referencia, status FROM pagamento WHERE id_pagamento = %s", (id_pagamento,))
        atual = cursor.fetchone()
        
        # Atualizar o pagamento com os novos dados, mantendo os valores atuais se não fornecidos
        cursor.execute(
            """
            UPDATE pagamento
            SET id_aluno = %s, data_pagamento = %s, valor_pago = %s, forma_pagamento = %s, referencia = %s, status = %s
            WHERE id_pagamento = %s
            """,
            (
                data.get('id_aluno', atual[0]),
                data.get('data_pagamento', atual[1]),
                data.get('valor_pago', atual[2]),
                data.get('forma_pagamento', atual[3]),
                data.get('referencia', atual[4]),
                data.get('status', atual[5]),
                id_pagamento
            )
        )
        conn.commit()
        return jsonify({"message": "Pagamento atualizado com sucesso"}), 200
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()
        conn.close()

@app.route('/pagamentos/<int:id_pagamento>', methods=['DELETE'])
@swag_from({
    'tags': ['Pagamentos'],
    'description': 'Deleta um pagamento pelo ID.',
    'parameters': [{
        'name': 'id_pagamento',
        'in': 'path',
        'required': True,
        'type': 'integer'
    }],
    'responses': {
        200: {'description': 'Pagamento deletado com sucesso'},
        400: {'description': 'Erro na requisição ou pagamento pendente'},
        404: {'description': 'Pagamento não encontrado'},
        500: {'description': 'Erro no servidor'}
    }
})
def delete_pagamento(id_pagamento):
    conn = create_connection()
    if not conn:
        return jsonify({"error": "Não foi possível conectar ao banco de dados"}), 500
        
    cursor = conn.cursor()
    try:
        # Verificar se o pagamento existe
        cursor.execute("SELECT status FROM pagamento WHERE id_pagamento = %s", (id_pagamento,))
        pagamento = cursor.fetchone()
        if pagamento is None:
            return jsonify({"error": "Pagamento não encontrado"}), 404
            
        # Verificar se o pagamento está pendente
        if pagamento[0] == 'pendente':
            return jsonify({"error": "Não é possível excluir um pagamento pendente"}), 400
            
        # Excluir o pagamento
        cursor.execute("DELETE FROM pagamento WHERE id_pagamento = %s", (id_pagamento,))
        conn.commit()
        return jsonify({"message": "Pagamento deletado com sucesso"}), 200
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()
        conn.close()