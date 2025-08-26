from flask import Flask, render_template
from .main import main as main_bp
from .admin import admin as admin_bp
from .extensions import db, login_manager
from flask_migrate import Migrate

def create_app():
    app = Flask(__name__)
    app.secret_key = 'secret'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///meu_banco.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    print("SQLALCHEMY_DATABASE_URI:", app.config['SQLALCHEMY_DATABASE_URI'])
    print("app.instance_path:", app.instance_path)
    print("app.root_path:", app.root_path)

    db.init_app(app)
    migrate = Migrate(app, db)

    login_manager.init_app(app)
    login_manager.login_view = 'main.login'

    # Garante que as tabelas existem
    with app.app_context():
        db.create_all()

    app.register_blueprint(main_bp)
    app.register_blueprint(admin_bp, url_prefix='/admin')

    # Handlers globais de erro

    @app.errorhandler(404)
    def erro_404(e):
        return render_template("erro.html", codigo=404, mensagem="Página não encontrada."), 404

    @app.errorhandler(405)
    def erro_405(e):
        return render_template("erro.html", codigo=405, mensagem="Método não permitido."), 405

    @app.errorhandler(500)
    def erro_500(e):
        return render_template("erro.html", codigo=500, mensagem="Ocorreu um erro inesperado no servidor."), 500

    @app.errorhandler(502)
    def erro_502(e):
        return render_template("erro.html", codigo=502, mensagem="Erro de gateway."), 502

    @app.errorhandler(503)
    def erro_503(e):
        return render_template("erro.html", codigo=503, mensagem="Serviço indisponível."), 503

    @app.errorhandler(504)
    def erro_504(e):
        return render_template("erro.html", codigo=504, mensagem="Tempo limite excedido."), 504


    return app