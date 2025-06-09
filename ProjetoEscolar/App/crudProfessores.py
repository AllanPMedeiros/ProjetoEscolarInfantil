from flask import Blueprint, request, jsonify
from App.Utils.bd import create_connection

# Blueprint para rotas de professores
app = Blueprint('professores', __name__)

@app.route('/professores', methods=['POST'])
def create_professor():
    data = request.get_json()
    conn = create_connection()
    if conn is None:
        return jsonify({"error": "Falha na conexão com o banco de dados"}), 500
    
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            INSERT INTO Professor (nome_completo, email, telefone)
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
def read_professor(id_professor):
    conn = create_connection()
    if conn is None:
        return jsonify({"error": "Falha na conexão com o banco de dados"}), 500
    
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM Professor WHERE id_professor = %s", (id_professor,))
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
def read_all_professores():
    conn = create_connection()
    if conn is None:
        return jsonify({"error": "Falha na conexão com o banco de dados"}), 500
    
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM Professor ORDER BY nome_completo")
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
def update_professor(id_professor):
    data = request.get_json()
    conn = create_connection()
    if conn is None:
        return jsonify({"error": "Falha na conexão com o banco de dados"}), 500
    
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            UPDATE Professor
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
def delete_professor(id_professor):
    conn = create_connection()
    if conn is None:
        return jsonify({"error": "Falha na conexão com o banco de dados"}), 500
    
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM Professor WHERE id_professor = %s", (id_professor,))
        conn.commit()
        if cursor.rowcount == 0:
            return jsonify({"error": "Professor não encontrado"}), 404
        return jsonify({"message": "Professor deletado com sucesso"}), 200
    except Exception as e:
        conn.rollback()
        print(f"Erro ao deletar professor: {str(e)}")
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()
        conn.close()