# Arquivo __init__.py para tornar a pasta app um pacote Python.
from flask import Flask
from flasgger import Swagger

def create_App(teste_config=None):
    App = Flask(__name__)

    if teste_config is None:
        App.config.from_mapping(
            SECRET_KEY='dev',
            DATABASE='escola'
        )
    else:
        App.config.update(teste_config)
    
    # Configuração do Swagger
    swagger_config = {
        "headers": [],
        "specs": [
            {
                "endpoint": "apispec",
                "route": "/apispec.json",
                "rule_filter": lambda rule: True,
                "model_filter": lambda tag: True,
            }
        ],
        "static_url_path": "/flasgger_static",
        "swagger_ui": True,
        "specs_route": "/docs/"
    }
    
    swagger_template = {
        "swagger": "2.0",
        "info": {
            "title": "API Escola",
            "description": "API para gerenciamento de escola",
            "version": "1.0.0"
        }
    }
    
    Swagger(App, config=swagger_config, template=swagger_template)
    
    # Registrar blueprints
    def register_blueprints(app):
        try:
            from .crudAlunos import app as crud_alunos_app
            from .crudAtividade_Aluno import app as crud_atividade_aluno_app 
            from .crudAtividades import app as crud_atividades_app
            from .crudPagamentos import app as crud_pagamentos_app
            from .crudPresencas import app as crud_presencas_app
            from .crudProfessores import app as crud_professores_app
            from .crudTurmas import app as crud_turmas_app
            from .crudUsuarios import app as crud_usuarios_app

            app.register_blueprint(crud_alunos_app)
            app.register_blueprint(crud_atividade_aluno_app)
            app.register_blueprint(crud_atividades_app)
            app.register_blueprint(crud_pagamentos_app)
            app.register_blueprint(crud_presencas_app)
            app.register_blueprint(crud_professores_app)
            app.register_blueprint(crud_turmas_app)
            app.register_blueprint(crud_usuarios_app)
        except ImportError as e:
            print(f"Erro ao importar módulos: {e}")
    
    # Registrar blueprints após a criação da aplicação
    register_blueprints(App)
    
    return App