import pytest
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Flask

@pytest.fixture
def app():
    app = Flask(__name__)
    app.config['TESTING'] = True
    
    from App.crudAlunos import app as alunos_bp
    from App.crudProfessores import app as professores_bp
    from App.crudTurmas import app as turmas_bp
    from App.crudUsuarios import app as usuarios_bp
    from App.crudPagamentos import app as pagamentos_bp
    from App.crudPresencas import app as presencas_bp
    from App.crudAtividades import app as atividades_bp
    from App.crudAtividade_Aluno import app as atividade_aluno_bp
    
    app.register_blueprint(alunos_bp)
    app.register_blueprint(professores_bp)
    app.register_blueprint(turmas_bp)
    app.register_blueprint(usuarios_bp)
    app.register_blueprint(pagamentos_bp)
    app.register_blueprint(presencas_bp)
    app.register_blueprint(atividades_bp)
    app.register_blueprint(atividade_aluno_bp)
    
    return app

@pytest.fixture
def client(app):
    return app.test_client()