from flask import Blueprint, jsonify, request
from Model.disponibilidade_model import Disponibilidade

disponibilidade_bp = Blueprint('disponibilidade_bp', __name__)

@disponibilidade_bp.route('/disponibilidades', methods=['GET'])
def rota_listar_disponibilidades():
    response, status = Disponibilidade.listar_disponibilidades()
    return jsonify(response), status

@disponibilidade_bp.route('/disponibilidades/<int:id>', methods=['GET'])
def rota_obter_disponibilidade(id):
    response, status = Disponibilidade.obter_disponibilidade(id)
    return jsonify(response), status

@disponibilidade_bp.route('/disponibilidades', methods=['POST'])
def rota_adicionar_disponibilidade():
    dados = request.json
    response, status = Disponibilidade.adicionar_disponibilidade(dados)
    return jsonify(response), status

@disponibilidade_bp.route('/disponibilidades/<int:id>', methods=['PUT'])
def rota_atualizar_disponibilidade(id):
    dados = request.json
    dados['id'] = id
    response, status = Disponibilidade.atualizar_disponibilidade(dados)
    return jsonify(response), status

@disponibilidade_bp.route('/disponibilidades/<int:id>', methods=['DELETE'])
def rota_deletar_disponibilidade(id):
    response, status = Disponibilidade.deletar_disponibilidade(id)
    return jsonify(response), status

@disponibilidade_bp.route('/disponibilidades/dia/<string:data>', methods=['GET'])
def rota_listar_por_dia(data):
    response, status = Disponibilidade.listar_por_dia(data)
    return jsonify(response), status

@disponibilidade_bp.route('/disponibilidades/semana/<string:inicio>/<string:fim>', methods=['GET'])
def rota_listar_por_semana(inicio, fim):
    response, status = Disponibilidade.listar_por_semana(inicio, fim)
    return jsonify(response), status