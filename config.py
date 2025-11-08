import os
from flask import Flask, request, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)


CORS(app,
     resources={
         r"/*": {
             "origins": ["http://localhost:3000"],
             "supports_credentials": True,
             "always_send": True
         }
     })

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

    
@app.after_request
def add_cors_headers(response):
    """Garante headers CORS em todas as respostas"""
    if request.method == "OPTIONS":
        response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
        response.headers['Access-Control-Max-Age'] = '600'
    return response


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
