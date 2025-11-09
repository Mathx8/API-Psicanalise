from flask import Blueprint, jsonify, request
from werkzeug.security import generate_password_hash, check_password_hash
from Model.paciente_model import Paciente
from config import db

paciente_bp = Blueprint('paciente_bp', __name__)

# ================================================================
# ROTAS DE CRUD
# ================================================================

@paciente_bp.route('/pacientes', methods=['GET'])
def rota_listar_pacientes():
    response, status = Paciente.listar_pacientes()
    return jsonify(response), status


@paciente_bp.route('/pacientes/<int:id>', methods=['GET'])
def rota_obter_paciente(id):
    response, status = Paciente.obter_paciente(id)
    return jsonify(response), status


@paciente_bp.route('/pacientes', methods=['POST'])
def rota_adicionar_paciente():
    try:
        dados = request.get_json()

        # Garante que a senha seja armazenada com hash
        if 'senha_bash' in dados:
            dados['senha_bash'] = generate_password_hash(dados['senha_bash'])

        response, status = Paciente.adicionar_paciente(dados)
        return jsonify(response), status
    except Exception as e:
        print("ERRO AO ADICIONAR PACIENTE:", str(e))
        return jsonify({"erro": "Erro interno no servidor", "detalhe": str(e)}), 500


@paciente_bp.route('/pacientes/<int:id>', methods=['PUT'])
def rota_atualizar_paciente(id):
    try:
        dados = request.get_json()

        # Atualiza o hash da senha, se enviada
        if 'senha_bash' in dados:
            dados['senha_bash'] = generate_password_hash(dados['senha_bash'])

        response, status = Paciente.atualizar_paciente(id, dados)
        return jsonify(response), status
    except Exception as e:
        print("ERRO AO ATUALIZAR PACIENTE:", str(e))
        return jsonify({"erro": "Erro interno no servidor", "detalhe": str(e)}), 500


@paciente_bp.route('/pacientes/<int:id>', methods=['DELETE'])
def rota_deletar_paciente(id):
    response, status = Paciente.deletar_paciente(id)
    return jsonify(response), status


# ================================================================
# ROTA DE LOGIN
# ================================================================
@paciente_bp.route('/login/paciente', methods=['POST'])
def login_paciente():
    try:
        dados = request.get_json()
        email = dados.get("email")
        senha = dados.get("senha")

        if not email or not senha:
            return jsonify({"erro": "Email e senha são obrigatórios"}), 400

        paciente = Paciente.query.filter_by(email=email).first()
        if not paciente:
            return jsonify({"erro": "Paciente não encontrado"}), 404

        senha_salva = paciente.senha_bash

        # Verifica se é hash ou texto puro
        if senha_salva.startswith("pbkdf2:sha256:"):
            senha_ok = check_password_hash(senha_salva, senha)
        else:
            senha_ok = senha_salva == senha

        if not senha_ok:
            return jsonify({"erro": "Senha incorreta"}), 401

        # Atualiza automaticamente para hash se ainda estiver em texto puro
        if not senha_salva.startswith("pbkdf2:sha256:"):
            paciente.senha_bash = generate_password_hash(senha)
            db.session.commit()

        return jsonify({
            "mensagem": "Login bem-sucedido",
            "paciente": paciente.to_dict()
        }), 200

    except Exception as e:
        print("ERRO LOGIN PACIENTE:", str(e))
        return jsonify({"erro": "Erro interno no servidor", "detalhe": str(e)}), 500
