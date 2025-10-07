from flask import Blueprint, jsonify, request
from Model.laudo_model import Laudo

laudo_bp = Blueprint('laudo_bp', __name__)

@laudo_bp.route('/laudos', methods=['GET'])
def rota_listar_laudos():
    response, status = Laudo.listar_laudos()
    return jsonify(response), status

@laudo_bp.route('/laudos/<int:id>', methods=['GET'])
def rota_obter_laudo(id):
    response, status = Laudo.obter_laudo(id)
    return jsonify(response), status

@laudo_bp.route('/laudos', methods=['POST'])
def rota_adicionar_laudo():
    dados = request.json
    response, status = Laudo.adicionar_laudo(dados)
    return jsonify(response), status

@laudo_bp.route('/laudos/<int:id>', methods=['PUT'])
def rota_atualizar_laudo(id):
    dados = request.json
    dados['id'] = id 
    response, status = Laudo.atualizar_laudo(dados)
    return jsonify(response), status

@laudo_bp.route('/laudos/<int:id>', methods=['DELETE'])
def rota_deletar_laudo(id):
    response, status = Laudo.deletar_laudo(id)
    return jsonify(response), status