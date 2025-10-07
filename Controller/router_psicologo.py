from flask import Blueprint, jsonify, request
from model.psicologo_model import Psicologo

psicologo_bp = Blueprint('psicologo_bp', __name__)

# =================== ROTAS ===================

@psicologo_bp.route('/psicologos', methods=['GET'])
def rota_listar_psicologos():
    response, status = Psicologo.listar_psicologos()
    return jsonify(response), status


@psicologo_bp.route('/psicologos/<int:id>', methods=['GET'])
def rota_obter_psicologo(id):
    response, status = Psicologo.obter_psicologo(id)
    return jsonify(response), status


@psicologo_bp.route('/psicologos', methods=['POST'])
def rota_adicionar_psicologo():
    dados = request.json
    response, status = Psicologo.adicionar_psicologo(dados)
    return jsonify(response), status


@psicologo_bp.route('/psicologos/<int:id>', methods=['PUT'])
def rota_atualizar_psicologo(id):
    dados = request.json
    dados['id'] = id 
    response, status = Psicologo.atualizar_psicologo(dados)
    return jsonify(response), status


@psicologo_bp.route('/psicologos/<int:id>', methods=['DELETE'])
def rota_deletar_psicologo(id):
    response, status = Psicologo.deletar_psicologo(id)
    return jsonify(response), status
