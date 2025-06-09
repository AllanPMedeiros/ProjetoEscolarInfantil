from flask import Blueprint, request, jsonify
from App.Utils.bd import create_connection

app = Blueprint('crud_alunos_app', __name__)

@app.route('/alunos', methods=['POST'])
def create_aluno():
    data = request.get_json()
    
    # Validação dos dados de entrada
    if not data or 'aluno_id' not in data or 'nome' not in data:
        return jsonify({"error": "Os campos aluno_id e nome são obrigatórios"}), 400
    
    conn = create_connection()
    if not conn:
        return jsonify({"error": "Não foi possível conectar ao banco de dados"}), 500
        
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            INSERT INTO alunos (aluno_id, nome, endereco, cidade, estado, cep, pais, telefone)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """,
            (data['aluno_id'], data['nome'], data.get('endereco'), data.get('cidade'), 
             data.get('estado'), data.get('cep'), data.get('pais'), data.get('telefone'))
        )
        conn.commit()
        return jsonify({"message": "Aluno criado com sucesso"}), 201
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()
        conn.close()

@app.route('/alunos/<string:aluno_id>', methods=['GET'])
def read_aluno(aluno_id):
    conn = create_connection()
    if not conn:
        return jsonify({"error": "Não foi possível conectar ao banco de dados"}), 500
        
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM alunos WHERE aluno_id = %s", (aluno_id,))
        aluno = cursor.fetchone()
        if aluno is None:
            return jsonify({"error": "Aluno não encontrado"}), 404
        
        # Convertendo objetos não serializáveis (como datetime) para string
        result = {
            "aluno_id": aluno[0],
            "nome": aluno[1],
            "endereco": aluno[2],
            "cidade": aluno[3],
            "estado": aluno[4],
            "cep": aluno[5],
            "pais": aluno[6],
            "telefone": aluno[7]
        }
        
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()
        conn.close()

@app.route('/alunos', methods=['GET'])
def read_all_alunos():
    conn = create_connection()
    if not conn:
        return jsonify({"error": "Não foi possível conectar ao banco de dados"}), 500
        
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM alunos ORDER BY nome")
        alunos = cursor.fetchall()
        
        result = []
        for aluno in alunos:
            result.append({
                "aluno_id": aluno[0],
                "nome": aluno[1],
                "endereco": aluno[2],
                "cidade": aluno[3],
                "estado": aluno[4],
                "cep": aluno[5],
                "pais": aluno[6],
                "telefone": aluno[7]
            })
        
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()
        conn.close()

@app.route('/alunos/<string:aluno_id>', methods=['PUT'])
def update_aluno(aluno_id):
    data = request.get_json()
    
    # Validação dos dados de entrada
    if not data or 'nome' not in data:
        return jsonify({"error": "O campo nome é obrigatório"}), 400
    
    conn = create_connection()
    if not conn:
        return jsonify({"error": "Não foi possível conectar ao banco de dados"}), 500
        
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            UPDATE alunos
            SET nome = %s, endereco = %s, cidade = %s, estado = %s, cep = %s, pais = %s, telefone = %s
            WHERE aluno_id = %s
            """,
            (data['nome'], data.get('endereco'), data.get('cidade'), data.get('estado'),
             data.get('cep'), data.get('pais'), data.get('telefone'), aluno_id)
        )
        conn.commit()
        if cursor.rowcount == 0:
            return jsonify({"error": "Aluno não encontrado"}), 404
        return jsonify({"message": "Aluno atualizado com sucesso"}), 200
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()
        conn.close()

@app.route('/alunos/<string:aluno_id>', methods=['DELETE'])
def delete_aluno(aluno_id):
    conn = create_connection()
    if not conn:
        return jsonify({"error": "Não foi possível conectar ao banco de dados"}), 500
        
    cursor = conn.cursor()
    try:
        # Verificar se existem dependências antes de deletar
        cursor.execute("SELECT COUNT(*) FROM Pagamento WHERE id_aluno = %s", (aluno_id,))
        count = cursor.fetchone()[0]
        if count > 0:
            return jsonify({"error": "Não é possível excluir este aluno pois existem pagamentos associados a ele."}), 400
            
        cursor.execute("SELECT COUNT(*) FROM Presenca WHERE id_aluno = %s", (aluno_id,))
        count = cursor.fetchone()[0]
        if count > 0:
            return jsonify({"error": "Não é possível excluir este aluno pois existem presenças associadas a ele."}), 400
        
        # Se não houver dependências, prosseguir com a exclusão
        cursor.execute("DELETE FROM alunos WHERE aluno_id = %s", (aluno_id,))
        conn.commit()
        if cursor.rowcount == 0:
            return jsonify({"error": "Aluno não encontrado"}), 404
        return jsonify({"message": "Aluno deletado com sucesso"}), 200
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()
        conn.close()