from flask import Blueprint, request, jsonify
from App.Utils.bd import create_connection
import bcrypt
import re

app = Blueprint('usuarios', __name__)

def validar_senha(senha):
    """Verifica se a senha tem pelo menos 8 caracteres, incluindo letras e números"""
    if len(senha) < 8:
        return False
    if not re.search("[a-zA-Z]", senha) or not re.search("[0-9]", senha):
        return False
    return True

@app.route('/usuarios', methods=['POST'])
def create_usuario():
    data = request.get_json()
    
    # Validação de dados
    if not data or 'login' not in data or 'senha' not in data:
        return jsonify({"error": "Dados incompletos. Login e senha são obrigatórios"}), 400
    
    # Validação da senha
    if not validar_senha(data['senha']):
        return jsonify({"error": "Senha deve ter pelo menos 8 caracteres, incluindo letras e números"}), 400
    
    conn = create_connection()
    if not conn:
        return jsonify({"error": "Falha na conexão com o banco de dados"}), 500
    
    cursor = conn.cursor()
    try:
        # Verificar se o login já existe
        cursor.execute("SELECT COUNT(*) FROM Usuario WHERE login = %s", (data['login'],))
        if cursor.fetchone()[0] > 0:
            return jsonify({"error": "Login já existe"}), 400
        
        # Criptografia da senha usando bcrypt
        hashed_password = bcrypt.hashpw(data['senha'].encode('utf-8'), bcrypt.gensalt())
        
        cursor.execute(
            """
            INSERT INTO Usuario (login, senha, nivel_acesso, id_professor)
            VALUES (%s, %s, %s, %s)
            """,
            (data['login'], hashed_password.decode('utf-8'), data.get('nivel_acesso', 'usuario'), data.get('id_professor'))
        )
        conn.commit()
        return jsonify({"message": "Usuário criado com sucesso"}), 201
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()
        conn.close()

@app.route('/usuarios/<int:id_usuario>', methods=['GET'])
def read_usuario(id_usuario):
    conn = create_connection()
    if not conn:
        return jsonify({"error": "Falha na conexão com o banco de dados"}), 500
        
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT id_usuario, login, nivel_acesso, id_professor FROM Usuario WHERE id_usuario = %s", (id_usuario,))
        usuario = cursor.fetchone()
        if usuario is None:
            return jsonify({"error": "Usuário não encontrado"}), 404
        return jsonify({
            "id_usuario": usuario[0],
            "login": usuario[1],
            "nivel_acesso": usuario[2],
            "id_professor": usuario[3]
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()
        conn.close()

@app.route('/usuarios', methods=['GET'])
def read_all_usuarios():
    conn = create_connection()
    if not conn:
        return jsonify({"error": "Falha na conexão com o banco de dados"}), 500
        
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT id_usuario, login, nivel_acesso, id_professor FROM Usuario")
        usuarios = cursor.fetchall()
        
        result = []
        for usuario in usuarios:
            result.append({
                "id_usuario": usuario[0],
                "login": usuario[1],
                "nivel_acesso": usuario[2],
                "id_professor": usuario[3]
            })
        
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()
        conn.close()

@app.route('/usuarios/<int:id_usuario>', methods=['PUT'])
def update_usuario(id_usuario):
    data = request.get_json()
    
    # Validação básica
    if not data:
        return jsonify({"error": "Dados inválidos"}), 400
        
    conn = create_connection()
    if not conn:
        return jsonify({"error": "Falha na conexão com o banco de dados"}), 500
        
    cursor = conn.cursor()
    try:
        # Verificar se o usuário existe
        cursor.execute("SELECT * FROM Usuario WHERE id_usuario = %s", (id_usuario,))
        if cursor.fetchone() is None:
            return jsonify({"error": "Usuário não encontrado"}), 404
        
        # Se a senha for atualizada, validar e criptografar
        if 'senha' in data:
            if not validar_senha(data['senha']):
                return jsonify({"error": "Senha deve ter pelo menos 8 caracteres, incluindo letras e números"}), 400
            hashed_password = bcrypt.hashpw(data['senha'].encode('utf-8'), bcrypt.gensalt())
            password_value = hashed_password.decode('utf-8')
        else:
            # Manter a senha atual
            cursor.execute("SELECT senha FROM Usuario WHERE id_usuario = %s", (id_usuario,))
            password_value = cursor.fetchone()[0]
        
        # Se o login for atualizado, verificar duplicidade
        if 'login' in data:
            cursor.execute("SELECT COUNT(*) FROM Usuario WHERE login = %s AND id_usuario != %s", (data['login'], id_usuario))
            if cursor.fetchone()[0] > 0:
                return jsonify({"error": "Login já existe"}), 400
            login_value = data['login']
        else:
            cursor.execute("SELECT login FROM Usuario WHERE id_usuario = %s", (id_usuario,))
            login_value = cursor.fetchone()[0]
            
        nivel_acesso = data.get('nivel_acesso')
        id_professor = data.get('id_professor')
        
        cursor.execute(
            """
            UPDATE Usuario
            SET login = %s, senha = %s, nivel_acesso = %s, id_professor = %s
            WHERE id_usuario = %s
            """,
            (login_value, password_value, nivel_acesso, id_professor, id_usuario)
        )
        conn.commit()
        return jsonify({"message": "Usuário atualizado com sucesso"}), 200
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()
        conn.close()

@app.route('/usuarios/<int:id_usuario>', methods=['DELETE'])
def delete_usuario(id_usuario):
    conn = create_connection()
    if not conn:
        return jsonify({"error": "Falha na conexão com o banco de dados"}), 500
        
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM Usuario WHERE id_usuario = %s", (id_usuario,))
        conn.commit()
        if cursor.rowcount == 0:
            return jsonify({"error": "Usuário não encontrado"}), 404
        return jsonify({"message": "Usuário deletado com sucesso"}), 200
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()
        conn.close()

# Rota de autenticação
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    
    if not data or 'login' not in data or 'senha' not in data:
        return jsonify({"error": "Informe login e senha"}), 400
    
    conn = create_connection()
    if not conn:
        return jsonify({"error": "Falha na conexão com o banco de dados"}), 500
        
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT id_usuario, login, senha, nivel_acesso FROM Usuario WHERE login = %s", (data['login'],))
        usuario = cursor.fetchone()
        
        if not usuario:
            return jsonify({"error": "Usuário ou senha inválidos"}), 401
            
        # Verificar senha com bcrypt
        if bcrypt.checkpw(data['senha'].encode('utf-8'), usuario[2].encode('utf-8')):
            return jsonify({
                "id_usuario": usuario[0],
                "login": usuario[1],
                "nivel_acesso": usuario[3],
                "message": "Login bem-sucedido"
            }), 200
        else:
            return jsonify({"error": "Usuário ou senha inválidos"}), 401
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()
        conn.close()