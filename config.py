import os
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)

# ===================== CORS =====================
CORS(app, resources={r"/*": {
    "origins": [
        "http://localhost:3000",
        "https://clinica-psicologia.onrender.com"
    ],
    "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    "allow_headers": ["Content-Type", "Authorization"],
}})

# ===================== HTTPS FIX RENDER =====================
@app.before_request
def force_https():
    if request.headers.get("X-Forwarded-Proto") == "http":
        return "Upgrade Required", 426

# ===================== BANCO =====================
db_path = os.path.join(os.getcwd(), "psicanalise.db")
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_path}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["JSON_SORT_KEYS"] = False

# ===================== SERVIDOR =====================
app.config["HOST"] = "0.0.0.0"
app.config["PORT"] = 5000
app.config["DEBUG"] = True

db = SQLAlchemy(app)
