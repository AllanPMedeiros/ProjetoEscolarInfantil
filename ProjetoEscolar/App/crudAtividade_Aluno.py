from flask import Blueprint, request, jsonify
from App.Utils.bd import create_connection

app = Blueprint('atividades_alunos', __name__)

# CRUD para Atividade_Aluno
@app.route('/atividades_alunos', methods=['POST'])
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
            INSERT INTO Atividade_Aluno (id_atividade, id_aluno)
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
def read_atividade_aluno(id_atividade, id_aluno):
    conn = create_connection()
    if not conn:
        return jsonify({"error": "Falha na conexão com o banco de dados"}), 500
        
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM Atividade_Aluno WHERE id_atividade = %s AND id_aluno = %s", (id_atividade, id_aluno))
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
def read_all_atividades_alunos():
    conn = create_connection()
    if not conn:
        return jsonify({"error": "Falha na conexão com o banco de dados"}), 500
        
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM Atividade_Aluno")
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
def delete_atividade_aluno(id_atividade, id_aluno):
    conn = create_connection()
    if not conn:
        return jsonify({"error": "Falha na conexão com o banco de dados"}), 500
        
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM Atividade_Aluno WHERE id_atividade = %s AND id_aluno = %s", (id_atividade, id_aluno))
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