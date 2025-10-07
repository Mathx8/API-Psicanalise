from flask import Blueprint, jsonify, request
from model.paciente_model import *

paciente_bp = Blueprint('paciente_bp', __name__)

@paciente_bp.route('/pacientes', methods=['GET'])
def rota_listar_pacientes():
    response, status = listar_pacientes()
    return jsonify(response), status

@paciente_bp.route('/pacientes/<int:id>', methods=['GET'])
def rota_obter_paciente(id):
    response, status = obter_paciente(id)
    return jsonify(response), status

@paciente_bp.route('/pacientes', methods=['POST'])
def rota_adicionar_paciente():
    dados = request.get_json()
    response, status = adicionar_paciente(dados)
    return jsonify(response), status

@paciente_bp.route('/pacientes/<int:id>', methods=['PUT'])
def rota_atualizar_paciente(id):
    dados = request.get_json()
    response, status = atualizar_paciente(id, dados)
    return jsonify(response), status

@paciente_bp.route('/pacientes/<int:id>', methods=['DELETE'])
def rota_deletar_paciente(id):
    response, status = deletar_paciente(id)
    return jsonify(response), status
