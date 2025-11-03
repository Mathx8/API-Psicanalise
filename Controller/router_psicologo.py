from flask import Blueprint, jsonify, request
from Model.psicologo_model import Psicologo
from Model.terapia_model import Terapia

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

@psicologo_bp.route('/login/psicologo', methods=['POST'])
def login_psicologo():
    dados = request.json
    login = dados.get("login")
    senha = dados.get("senha")

    if not login or not senha:
        return jsonify({"erro": "Email/CRP e senha são obrigatórios"}), 400

    psicologo = Psicologo.query.filter(
        (Psicologo.email == login) | (Psicologo.crp == login)
    ).first()

    if not psicologo:
        return jsonify({"erro": "Usuário não encontrado"}), 404

    if psicologo.senha_bash != senha:
        return jsonify({"erro": "Senha incorreta"}), 401

    return jsonify({
        "mensagem": "Login bem-sucedido",
        "psicologo": psicologo.to_dict()
    }), 200

@psicologo_bp.route('/psicologos/<int:id_psicologo>/pacientes', methods=['GET'])
def rota_listar_pacientes_por_psicologo(id_psicologo):
    """Listar todos os pacientes atendidos por um psicólogo"""
    response, status = Terapia.listar_pacientes_por_psicologo(id_psicologo)
    return jsonify(response), status