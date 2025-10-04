import sys
import os

# =================== AJUSTE DE PATH PARA IMPORT ===================
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config import app, db
from controller.router_paciente import paciente_bp

# =================== REGISTRAR ROTAS ===================
app.register_blueprint(paciente_bp)

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
