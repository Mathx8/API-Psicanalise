from flask import Blueprint, jsonify, request
from model.sala_model import Sala

sala_bp = Blueprint('sala_bp', __name__)

@sala_bp.route('/salas', methods=['GET'])
def rota_listar_salas():
    response, status = Sala.listar_salas()
    return jsonify(response), status

@sala_bp.route('/salas/<int:id>', methods=['GET'])
def rota_obter_sala(id):
    response, status = Sala.obter_sala(id)
    return jsonify(response), status

@sala_bp.route('/salas', methods=['POST'])
def rota_adicionar_sala():
    dados = request.json
    response, status = Sala.adicionar_sala(dados)
    return jsonify(response), status

@sala_bp.route('/salas/<int:id>', methods=['PUT'])
def rota_atualizar_sala(id):
    dados = request.json
    dados['id'] = id 
    response, status = Sala.atualizar_sala(dados)
    return jsonify(response), status

@sala_bp.route('/salas/<int:id>', methods=['DELETE'])
def rota_deletar_sala(id):
    response, status = Sala.deletar_sala(id)
    return jsonify(response), status