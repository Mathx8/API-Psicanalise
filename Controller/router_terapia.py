from flask import Blueprint, jsonify, request
from model.terapia_model import Terapia

terapia_bp = Blueprint('terapia_bp', __name__)

@terapia_bp.route('/terapias', methods=['GET'])
def rota_listar_terapias():
    response, status = Terapia.listar_terapias()
    return jsonify(response), status

@terapia_bp.route('/terapias/<int:id>', methods=['GET'])
def rota_obter_terapia(id):
    response, status = Terapia.obter_terapia(id)
    return jsonify(response), status

@terapia_bp.route('/terapias', methods=['POST'])
def rota_adicionar_terapia():
    dados = request.json
    response, status = Terapia.adicionar_terapia(dados)
    return jsonify(response), status

@terapia_bp.route('/terapias/<int:id>', methods=['PUT'])
def rota_atualizar_terapia(id):
    dados = request.json
    dados['id'] = id
    response, status = Terapia.atualizar_terapia(dados)
    return jsonify(response), status

@terapia_bp.route('/terapias/<int:id>', methods=['DELETE'])
def rota_deletar_terapia(id):
    response, status = Terapia.deletar_terapia(id)
    return jsonify(response), status

@terapia_bp.route('/terapias/dia/<string:data>', methods=['GET'])
def rota_listar_por_dia(data):
    psicologo_id = request.args.get('psicologo_id', type=int)
    response, status = Terapia.listar_por_dia(data, psicologo_id)
    return jsonify(response), status

@terapia_bp.route('/terapias/semana/<string:inicio>/<string:fim>', methods=['GET'])
def rota_listar_por_semana(inicio, fim):
    psicologo_id = request.args.get('psicologo_id', type=int)
    response, status = Terapia.listar_por_semana(inicio, fim, psicologo_id)
    return jsonify(response), status