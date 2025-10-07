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
