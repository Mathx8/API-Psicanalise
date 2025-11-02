from flask import Blueprint, jsonify, request
from Model.paciente_model import Paciente

paciente_bp = Blueprint('paciente_bp', __name__)

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
    dados = request.get_json()
    response, status = Paciente.adicionar_paciente(dados)
    return jsonify(response), status

@paciente_bp.route('/pacientes/<int:id>', methods=['PUT'])
def rota_atualizar_paciente(id):
    dados = request.get_json()
    response, status = Paciente.atualizar_paciente(id, dados)
    return jsonify(response), status

@paciente_bp.route('/pacientes/<int:id>', methods=['DELETE'])
def rota_deletar_paciente(id):
    response, status = Paciente.deletar_paciente(id)
    return jsonify(response), status

@paciente_bp.route('/login/paciente', methods=['POST'])
def login_paciente():
    dados = request.get_json()
    email = dados.get("email")
    senha = dados.get("senha")

    if not email or not senha:
        return jsonify({"erro": "Email e senha são obrigatórios"}), 400

    paciente = Paciente.query.filter_by(email=email).first()

    if not paciente:
        return jsonify({"erro": "Paciente não encontrado"}), 404

    if paciente.senha != senha:
        return jsonify({"erro": "Senha incorreta"}), 401

    return jsonify({
        "mensagem": "Login bem-sucedido",
        "paciente": paciente.to_dict()
    }), 200