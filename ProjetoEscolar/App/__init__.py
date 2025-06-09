# Arquivo __init__.py para tornar a pasta app um pacote Python.
from flask import Flask

def create_app(teste_config=None):
    app = Flask(__name__)

    if teste_config is None:
        app.config.from_mapping(
            SECRET_KEY='dev',
            DATABASE='escola'
        )
    else:
        app.config.update(teste_config)
    
    from App.crudAlunos import app as crud_alunos_app
    from App.crudAtividade_Aluno import app as crud_atividade_aluno_app
    from App.crudAtividades import app as crud_atividades_app
    from App.crudPagamentos import app as crud_pagamentos_app
    from App.crudPresencas import app as crud_presencas_app
    from App.crudProfessores import app as crud_professores_app
    from App.crudTurmas import app as crud_turmas_app
    from App.crudUsuarios import app as crud_usuarios_app

    app.register_blueprint(crud_alunos_app)
    app.register_blueprint(crud_atividade_aluno_app)
    app.register_blueprint(crud_atividades_app)
    app.register_blueprint(crud_pagamentos_app)
    app.register_blueprint(crud_presencas_app)
    app.register_blueprint(crud_professores_app)
    app.register_blueprint(crud_turmas_app)
    app.register_blueprint(crud_usuarios_app)


    
    
    return app 