import os
from flask import Flask, request, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)

# ✅ Configuração CORS limpa e compatível com Flask-CORS
CORS(app, resources={r"/*": {"origins": ["http://localhost:3000", "https://clinica-psicologia-lovat.vercel.app/"]}},
     supports_credentials=True)

@app.before_request
def enforce_https():
    """Redirecionamento HTTPS inteligente para o Render"""
    if request.method == "OPTIONS":
        return
    
    is_https = (
        request.is_secure or 
        request.headers.get('X-Forwarded-Proto', 'https') == 'https'
    )
    if not is_https and 'localhost' not in request.host:
        https_url = request.url.replace('http://', 'https://', 1)
        return redirect(https_url, code=301)

# ⚠️ REMOVA o after_request de CORS
# Flask-CORS já cuida automaticamente dos OPTIONS e dos headers
# Se quiser apenas registrar algo específico, pode, mas sem sobrescrever CORS.

# =================== CAMINHO ABSOLUTO DO BANCO ===================
db_path = os.path.join(os.getcwd(), "psicanalise.db")
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_path}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["JSON_SORT_KEYS"] = False

# =================== CONFIG SERVIDOR ===================
app.config["HOST"] = "0.0.0.0"
app.config["PORT"] = 5000
app.config["DEBUG"] = True

# =================== INSTÂNCIA DB ===================
db = SQLAlchemy(app)
