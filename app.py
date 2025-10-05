import sys
import os

# =================== AJUSTE DE PATH PARA IMPORT ===================
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config import app, db
from Controller.router_paciente import paciente_bp
from Controller.router_psicologo import psicologo_bp
from Controller.router_sala import sala_bp
from Controller.router_disponibilidade import disponibilidade_bp
from Controller.router_terapia import terapia_bp
from Controller.router_laudo import laudo_bp

# =================== REGISTRAR ROTAS ===================
app.register_blueprint(paciente_bp)
app.register_blueprint(psicologo_bp)
app.register_blueprint(sala_bp)
app.register_blueprint(disponibilidade_bp)
app.register_blueprint(terapia_bp)
app.register_blueprint(laudo_bp)

# =================== CRIAR TABELAS ===================
with app.app_context():
    db.create_all()
    print(f"Banco de dados criado com sucesso em: {os.path.join(os.getcwd(), 'psicanalise.db')}")

# =================== INICIAR SERVIDOR ===================
if __name__ == '__main__':
    app.run(
        host=app.config['HOST'],
        port=app.config['PORT'],
        debug=app.config['DEBUG']
    )
