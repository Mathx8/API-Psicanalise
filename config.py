import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

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
