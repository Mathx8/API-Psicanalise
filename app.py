from flask import Flask
from database import db
from Controller.paciente_routes import paciente_bp

def create_app():
    app = Flask(__name__)

    # Configuração simples para SQLite local
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///banco.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    # Registro das rotas (Blueprint)
    app.register_blueprint(paciente_bp, url_prefix="/pacientes")

    # Inicializa o banco de dados na primeira execução
    with app.app_context():
        db.create_all()

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
