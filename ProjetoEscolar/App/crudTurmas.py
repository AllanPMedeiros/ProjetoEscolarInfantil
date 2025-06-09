from flask import Blueprint, request, jsonify
from App.Utils.bd import create_connection

app = Blueprint('turmas', __name__)

@app.route('/turmas', methods=['POST'])
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
            cursor.execute("SELECT COUNT(*) FROM Professor WHERE id_professor = %s", (data['id_professor'],))
            if cursor.fetchone()[0] == 0:
                return jsonify({"error": "Professor não encontrado"}), 400
        
        cursor.execute(
            """
            INSERT INTO Turma (nome_turma, id_professor, horario)
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
def read_turma(id_turma):
    conn = create_connection()
    if not conn:
        return jsonify({"error": "Falha na conexão com o banco de dados"}), 500
        
    cursor = conn.cursor()
    try:
        cursor.execute("""
            SELECT t.id_turma, t.nome_turma, t.id_professor, t.horario, p.nome_completo as nome_professor
            FROM Turma t
            LEFT JOIN Professor p ON t.id_professor = p.id_professor
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
def read_all_turmas():
    conn = create_connection()
    if not conn:
        return jsonify({"error": "Falha na conexão com o banco de dados"}), 500
        
    cursor = conn.cursor()
    try:
        cursor.execute("""
            SELECT t.id_turma, t.nome_turma, t.id_professor, t.horario, p.nome_completo as nome_professor
            FROM Turma t
            LEFT JOIN Professor p ON t.id_professor = p.id_professor
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
        cursor.execute("SELECT COUNT(*) FROM Turma WHERE id_turma = %s", (id_turma,))
        if cursor.fetchone()[0] == 0:
            return jsonify({"error": "Turma não encontrada"}), 404
            
        # Verificar se o professor existe, caso tenha sido informado
        if 'id_professor' in data and data['id_professor']:
            cursor.execute("SELECT COUNT(*) FROM Professor WHERE id_professor = %s", (data['id_professor'],))
            if cursor.fetchone()[0] == 0:
                return jsonify({"error": "Professor não encontrado"}), 400
                
        cursor.execute(
            """
            UPDATE Turma
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
def delete_turma(id_turma):
    conn = create_connection()
    if not conn:
        return jsonify({"error": "Falha na conexão com o banco de dados"}), 500
        
    cursor = conn.cursor()
    try:
        # Verificar se há alunos associados à turma
        cursor.execute("SELECT COUNT(*) FROM Aluno_Turma WHERE id_turma = %s", (id_turma,))
        if cursor.fetchone()[0] > 0:
            return jsonify({"error": "Não é possível excluir a turma pois possui alunos associados"}), 400
            
        cursor.execute("DELETE FROM Turma WHERE id_turma = %s", (id_turma,))
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