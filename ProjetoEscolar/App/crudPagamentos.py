from flask import Blueprint, request, jsonify
from App.Utils.bd import create_connection
import datetime

app = Blueprint('pagamentos', __name__)

@app.route('/pagamentos', methods=['POST'])
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
        cursor.execute("SELECT COUNT(*) FROM alunos WHERE aluno_id = %s", (data['id_aluno'],))
        if cursor.fetchone()[0] == 0:
            return jsonify({"error": "Aluno não encontrado"}), 404
            
        cursor.execute(
            """
            INSERT INTO Pagamento (id_aluno, data_pagamento, valor_pago, forma_pagamento, referencia, status)
            VALUES (%s, %s, %s, %s, %s, %s)
            """,
            (data['id_aluno'], data['data_pagamento'], data['valor_pago'], 
             data.get('forma_pagamento'), data.get('referencia'), data.get('status', 'Pendente'))
        )
        conn.commit()
        return jsonify({"message": "Pagamento criado com sucesso"}), 201
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()
        conn.close()

@app.route('/pagamentos/<int:id_pagamento>', methods=['GET'])
def read_pagamento(id_pagamento):
    conn = create_connection()
    if not conn:
        return jsonify({"error": "Não foi possível conectar ao banco de dados"}), 500
        
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM Pagamento WHERE id_pagamento = %s", (id_pagamento,))
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
        query = "SELECT * FROM Pagamento"
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
        cursor.execute("SELECT * FROM Pagamento WHERE id_pagamento = %s", (id_pagamento,))
        if cursor.fetchone() is None:
            return jsonify({"error": "Pagamento não encontrado"}), 404
            
        # Verificar se o aluno existe, se estiver sendo atualizado
        if 'id_aluno' in data:
            cursor.execute("SELECT COUNT(*) FROM alunos WHERE aluno_id = %s", (data['id_aluno'],))
            if cursor.fetchone()[0] == 0:
                return jsonify({"error": "Aluno não encontrado"}), 404
                
        # Obter os valores atuais
        cursor.execute("SELECT id_aluno, data_pagamento, valor_pago, forma_pagamento, referencia, status FROM Pagamento WHERE id_pagamento = %s", (id_pagamento,))
        atual = cursor.fetchone()
        
        # Atualizar o pagamento com os novos dados, mantendo os valores atuais se não fornecidos
        cursor.execute(
            """
            UPDATE Pagamento
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
def delete_pagamento(id_pagamento):
    conn = create_connection()
    if not conn:
        return jsonify({"error": "Não foi possível conectar ao banco de dados"}), 500
        
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM Pagamento WHERE id_pagamento = %s", (id_pagamento,))
        conn.commit()
        if cursor.rowcount == 0:
            return jsonify({"error": "Pagamento não encontrado"}), 404
        return jsonify({"message": "Pagamento deletado com sucesso"}), 200
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()
        conn.close()