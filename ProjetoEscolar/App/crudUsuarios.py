from flask import Blueprint, request, jsonify
from .Utils.bd import create_connection
import bcrypt
import re
from flasgger import swag_from

app = Blueprint('usuarios', __name__)

def validar_senha(senha):
    """Verifica se a senha tem pelo menos 8 caracteres, incluindo letras e números"""
    if len(senha) < 8:
        return False
    if not re.search("[a-zA-Z]", senha) or not re.search("[0-9]", senha):
        return False
    return True

@app.route('/usuarios', methods=['POST'])
@swag_from({
    'tags': ['Usuários'],
    'description': 'Cria um novo usuário.',
    'parameters': [{
        'name': 'body',
        'in': 'body',
        'required': True,
        'schema': {
            'type': 'object',
            'properties': {
                'login': {'type': 'string'},
                'senha': {'type': 'string'},
                'nivel_acesso': {'type': 'string'},
                'id_professor': {'type': 'integer'}
            },
            'required': ['login', 'senha'],
            'example': {
                'login': '',
                'senha': '',
                'nivel_acesso': '',
                'id_professor': 0
            }
        }
    }],
    'responses': {
        201: {
            'description': 'Usuário criado com sucesso',
            'schema': {
                'type': 'object',
                'properties': {
                    'message': {'type': 'string'},
                    'id_usuario': {'type': 'integer'}
                }
            }
        },
        400: {'description': 'Erro na requisição ou dados inválidos'},
        500: {'description': 'Erro no servidor'}
    }
})
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
        cursor.execute("SELECT COUNT(*) FROM usuario WHERE login = %s", (data['login'],))
        if cursor.fetchone()[0] > 0:
            return jsonify({"error": "Login já existe"}), 400
        
        # Criptografia da senha usando bcrypt
        hashed_password = bcrypt.hashpw(data['senha'].encode('utf-8'), bcrypt.gensalt())
        
        cursor.execute(
            """
            INSERT INTO usuario (login, senha, nivel_acesso, id_professor)
            VALUES (%s, %s, %s, %s)
            RETURNING id_usuario
            """,
            (data['login'], hashed_password.decode('utf-8'), data.get('nivel_acesso', 'usuario'), data.get('id_professor'))
        )
        id_usuario = cursor.fetchone()[0]
        conn.commit()
        return jsonify({"message": "Usuário criado com sucesso", "id_usuario": id_usuario}), 201
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()
        conn.close()

@app.route('/usuarios/<int:id_usuario>', methods=['GET'])
@swag_from({
    'tags': ['Usuários'],
    'description': 'Busca um usuário pelo ID.',
    'parameters': [{
        'name': 'id_usuario',
        'in': 'path',
        'required': True,
        'type': 'integer'
    }],
    'responses': {
        200: {
            'description': 'Dados do usuário',
            'schema': {
                'type': 'object',
                'properties': {
                    'id_usuario': {'type': 'integer'},
                    'login': {'type': 'string'},
                    'nivel_acesso': {'type': 'string'},
                    'id_professor': {'type': 'integer'}
                }
            }
        },
        404: {'description': 'Usuário não encontrado'},
        500: {'description': 'Erro no servidor'}
    }
})
def read_usuario(id_usuario):
    conn = create_connection()
    if not conn:
        return jsonify({"error": "Falha na conexão com o banco de dados"}), 500
        
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT id_usuario, login, nivel_acesso, id_professor FROM usuario WHERE id_usuario = %s", (id_usuario,))
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
@swag_from({
    'tags': ['Usuários'],
    'description': 'Lista todos os usuários cadastrados.',
    'responses': {
        200: {
            'description': 'Lista de usuários',
            'schema': {
                'type': 'array',
                'items': {
                    'type': 'object',
                    'properties': {
                        'id_usuario': {'type': 'integer'},
                        'login': {'type': 'string'},
                        'nivel_acesso': {'type': 'string'},
                        'id_professor': {'type': 'integer'}
                    }
                }
            }
        },
        500: {'description': 'Erro no servidor'}
    }
})
def read_all_usuarios():
    conn = create_connection()
    if not conn:
        return jsonify({"error": "Falha na conexão com o banco de dados"}), 500
        
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT id_usuario, login, nivel_acesso, id_professor FROM usuario")
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
@swag_from({
    'tags': ['Usuários'],
    'description': 'Atualiza os dados de um usuário.',
    'parameters': [
        {
            'name': 'id_usuario',
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
                    'login': {'type': 'string'},
                    'senha': {'type': 'string'},
                    'nivel_acesso': {'type': 'string'},
                    'id_professor': {'type': 'integer'}
                },
                'example': {
                    'login': '',
                    'senha': '',
                    'nivel_acesso': '',
                    'id_professor': 0
                }
            }
        }
    ],
    'responses': {
        200: {'description': 'Usuário atualizado com sucesso'},
        400: {'description': 'Erro na requisição ou dados inválidos'},
        404: {'description': 'Usuário não encontrado'},
        500: {'description': 'Erro no servidor'}
    }
})
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
        cursor.execute("SELECT * FROM usuario WHERE id_usuario = %s", (id_usuario,))
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
            cursor.execute("SELECT senha FROM usuario WHERE id_usuario = %s", (id_usuario,))
            password_value = cursor.fetchone()[0]
        
        # Se o login for atualizado, verificar duplicidade
        if 'login' in data:
            cursor.execute("SELECT COUNT(*) FROM usuario WHERE login = %s AND id_usuario != %s", (data['login'], id_usuario))
            if cursor.fetchone()[0] > 0:
                return jsonify({"error": "Login já existe"}), 400
            login_value = data['login']
        else:
            cursor.execute("SELECT login FROM usuario WHERE id_usuario = %s", (id_usuario,))
            login_value = cursor.fetchone()[0]
            
        nivel_acesso = data.get('nivel_acesso')
        id_professor = data.get('id_professor')
        
        cursor.execute(
            """
            UPDATE usuario
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
@swag_from({
    'tags': ['Usuários'],
    'description': 'Deleta um usuário pelo ID.',
    'parameters': [{
        'name': 'id_usuario',
        'in': 'path',
        'required': True,
        'type': 'integer'
    }],
    'responses': {
        200: {'description': 'Usuário deletado com sucesso'},
        404: {'description': 'Usuário não encontrado'},
        500: {'description': 'Erro no servidor'}
    }
})
def delete_usuario(id_usuario):
    conn = create_connection()
    if not conn:
        return jsonify({"error": "Falha na conexão com o banco de dados"}), 500
        
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM usuario WHERE id_usuario = %s", (id_usuario,))
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
# @app.route('/login', methods=['POST'])
# @swag_from({
#     'tags': ['Autenticação'],
#     'description': 'Autentica um usuário no sistema.',
#     'parameters': [{
#         'name': 'body',
#         'in': 'body',
#         'required': True,
#         'schema': {
#             'type': 'object',
#             'properties': {
#                 'login': {'type': 'string'},
#                 'senha': {'type': 'string'}
#             },
#             'required': ['login', 'senha'],
#             'example': {
#                 'login': '',
#                 'senha': ''
#             }
#         }
#     }],
#     'responses': {
#         200: {
#             'description': 'Login bem-sucedido',
#             'schema': {
#                 'type': 'object',
#                 'properties': {
#                     'id_usuario': {'type': 'integer'},
#                     'login': {'type': 'string'},
#                     'nivel_acesso': {'type': 'string'},
#                     'message': {'type': 'string'}
#                 }
#             }
#         },
#         400: {'description': 'Dados incompletos'},
#         401: {'description': 'Usuário ou senha inválidos'},
#         500: {'description': 'Erro no servidor'}
#     }
# })
# def login():
#     data = request.get_json()
    
#     if not data or 'login' not in data or 'senha' not in data:
#         return jsonify({"error": "Informe login e senha"}), 400
    
#     conn = create_connection()
#     if not conn:
#         return jsonify({"error": "Falha na conexão com o banco de dados"}), 500
        
#     cursor = conn.cursor()
#     try:
#         cursor.execute("SELECT id_usuario, login, senha, nivel_acesso FROM usuario WHERE login = %s", (data['login'],))
#         usuario = cursor.fetchone()
        
#         if not usuario:
#             return jsonify({"error": "Usuário ou senha inválidos"}), 401
            
#         # Verificar senha com bcrypt
#         if bcrypt.checkpw(data['senha'].encode('utf-8'), usuario[2].encode('utf-8')):
#             return jsonify({
#                 "id_usuario": usuario[0],
#                 "login": usuario[1],
#                 "nivel_acesso": usuario[3],
#                 "message": "Login bem-sucedido"
#             }), 200
#         else:
#             return jsonify({"error": "Usuário ou senha inválidos"}), 401
#     except Exception as e:
#         return jsonify({"error": str(e)}), 400
#     finally:
#         cursor.close()
#         conn.close()