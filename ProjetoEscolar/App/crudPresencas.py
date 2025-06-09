from flask import Blueprint, request, jsonify
from App.Utils.bd import create_connection
import datetime

app = Blueprint('presencas', __name__)

@app.route('/presencas', methods=['POST'])
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
        cursor.execute("SELECT COUNT(*) FROM alunos WHERE aluno_id = %s", (data['id_aluno'],))
        if cursor.fetchone()[0] == 0:
            return jsonify({"error": "Aluno não encontrado"}), 404
            
        # Verificar se já existe uma presença para este aluno nesta data
        cursor.execute(
            "SELECT COUNT(*) FROM Presenca WHERE id_aluno = %s AND data_presenca = %s",
            (data['id_aluno'], data['data_presenca'])
        )
        if cursor.fetchone()[0] > 0:
            return jsonify({"error": "Já existe um registro de presença para este aluno nesta data"}), 400
            
        cursor.execute(
            """
            INSERT INTO Presenca (id_aluno, data_presenca, presente)
            VALUES (%s, %s, %s)
            """,
            (data['id_aluno'], data['data_presenca'], data['presente'])
        )
        conn.commit()
        return jsonify({"message": "Presença registrada com sucesso"}), 201
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()
        conn.close()

@app.route('/presencas/<int:id_presenca>', methods=['GET'])
def read_presenca(id_presenca):
    conn = create_connection()
    if not conn:
        return jsonify({"error": "Não foi possível conectar ao banco de dados"}), 500
        
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM Presenca WHERE id_presenca = %s", (id_presenca,))
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
        query = "SELECT * FROM Presenca"
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
        cursor.execute("SELECT * FROM Presenca WHERE id_presenca = %s", (id_presenca,))
        presenca_atual = cursor.fetchone()
        if presenca_atual is None:
            return jsonify({"error": "Presença não encontrada"}), 404
            
        # Verificar se o aluno existe, se estiver sendo atualizado
        if 'id_aluno' in data:
            cursor.execute("SELECT COUNT(*) FROM alunos WHERE aluno_id = %s", (data['id_aluno'],))
            if cursor.fetchone()[0] == 0:
                return jsonify({"error": "Aluno não encontrado"}), 404
                
        # Verificar se já existe uma presença para este aluno nesta data (evitar duplicidade)
        if 'id_aluno' in data or 'data_presenca' in data:
            id_aluno = data.get('id_aluno', presenca_atual[1])
            data_presenca = data.get('data_presenca', presenca_atual[2])
            
            cursor.execute(
                """
                SELECT COUNT(*) FROM Presenca 
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
            UPDATE Presenca
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
def delete_presenca(id_presenca):
    conn = create_connection()
    if not conn:
        return jsonify({"error": "Não foi possível conectar ao banco de dados"}), 500
        
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM Presenca WHERE id_presenca = %s", (id_presenca,))
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