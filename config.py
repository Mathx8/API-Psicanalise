import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS  # ⬅️ Import necessário

app = Flask(__name__)

# =================== CONFIG CORS ===================
# Permite acesso de qualquer origem
CORS(app, resources={r"/*": {"origins": "*"}})

# =================== CAMINHO ABSOLUTO DO BANCO ===================
db_path = os.path.join(os.getcwd(), 'psicanalise.db')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSON_SORT_KEYS'] = False

# =================== CONFIG SERVIDOR ===================
app.config['HOST'] = '0.0.0.0'
app.config['PORT'] = 5000
app.config['DEBUG'] = True

# =================== INSTÂNCIA DB ===================
db = SQLAlchemy(app)
