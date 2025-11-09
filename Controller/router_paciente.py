from flask import Blueprint, jsonify, request
from Model.paciente_model import Paciente

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
        # Nenhum hash — senha é salva diretamente como enviada
        response, status = Paciente.adicionar_paciente(dados)
        return jsonify(response), status
    except Exception as e:
        print("ERRO AO ADICIONAR PACIENTE:", str(e))
        return jsonify({"erro": "Erro interno no servidor", "detalhe": str(e)}), 500


@paciente_bp.route('/pacientes/<int:id>', methods=['PUT'])
def rota_atualizar_paciente(id):
    try:
        dados = request.get_json()
        # Nenhum hash — senha é atualizada diretamente
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

        # Comparação direta (sem hash)
        if paciente.senha_bash != senha:
            return jsonify({"erro": "Senha incorreta"}), 401

        return jsonify({
            "mensagem": "Login bem-sucedido",
            "paciente": paciente.to_dict()
        }), 200

    except Exception as e:
        print("ERRO LOGIN PACIENTE:", str(e))
        return jsonify({
            "erro": "Erro interno no servidor",
            "detalhe": str(e)
        }), 500
