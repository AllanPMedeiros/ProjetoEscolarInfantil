from flask import Blueprint, request, jsonify
from App.Utils.bd import create_connection

app = Blueprint('atividades', __name__) 

@app.route('/atividades', methods=['POST'])
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
            INSERT INTO Atividade (descricao, data_realizacao)
            VALUES (%s, %s)
            """,
            (data['descricao'], data['data_realizacao'])
        )
        conn.commit()
        # Obter o ID gerado
        cursor.execute("SELECT LAST_INSERT_ID()")
        id_atividade = cursor.fetchone()[0]
        return jsonify({"message": "Atividade criada com sucesso", "id_atividade": id_atividade}), 201
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()
        conn.close()

@app.route('/atividades/<int:id_atividade>', methods=['GET'])
def read_atividade(id_atividade):
    conn = create_connection()
    if not conn:
        return jsonify({"error": "Falha na conexão com o banco de dados"}), 500
        
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM Atividade WHERE id_atividade = %s", (id_atividade,))
        atividade = cursor.fetchone()
        if atividade is None:
            return jsonify({"error": "Atividade não encontrada"}), 404
        return jsonify({
            "id_atividade": atividade[0],
            "descricao": atividade[1],
            "data_realizacao": atividade[2].strftime('%Y-%m-%d') if hasattr(atividade[2], 'strftime') else atividade[2]
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()
        conn.close()

@app.route('/atividades', methods=['GET'])
def read_all_atividades():
    conn = create_connection()
    if not conn:
        return jsonify({"error": "Falha na conexão com o banco de dados"}), 500
        
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM Atividade ORDER BY data_realizacao")
        atividades = cursor.fetchall()
        
        result = []
        for atividade in atividades:
            result.append({
                "id_atividade": atividade[0],
                "descricao": atividade[1],
                "data_realizacao": atividade[2].strftime('%Y-%m-%d') if hasattr(atividade[2], 'strftime') else atividade[2]
            })
        
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()
        conn.close()

@app.route('/atividades/<int:id_atividade>', methods=['PUT'])
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
            UPDATE Atividade
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
def delete_atividade(id_atividade):
    conn = create_connection()
    if not conn:
        return jsonify({"error": "Falha na conexão com o banco de dados"}), 500
        
    cursor = conn.cursor()
    try:
        # Verificar primeiro se existem relações em Atividade_Aluno
        cursor.execute("SELECT COUNT(*) FROM Atividade_Aluno WHERE id_atividade = %s", (id_atividade,))
        if cursor.fetchone()[0] > 0:
            return jsonify({"error": "Não é possível excluir a atividade pois está associada a alunos"}), 400
            
        cursor.execute("DELETE FROM Atividade WHERE id_atividade = %s", (id_atividade,))
        conn.commit()
        if cursor.rowcount == 0:
            return jsonify({"error": "Atividade não encontrada"}), 404
        return jsonify({"message": "Atividade deletada com sucesso"}), 200
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()
        conn.close()