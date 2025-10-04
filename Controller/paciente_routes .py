from flask import Blueprint, jsonify, request
from Model.paciente_model import PacienteModel
from database import db

paciente_bp = Blueprint("paciente_bp", __name__)

@paciente_bp.route("/", methods=["GET"])
def listar_pacientes():
    pacientes = PacienteModel.query.all()
    return jsonify([p.to_dict() for p in pacientes]), 200

@paciente_bp.route("/<int:id_paciente>", methods=["GET"])
def buscar_paciente(id_paciente):
    paciente = PacienteModel.query.get(id_paciente)
    if not paciente:
        return jsonify({"mensagem": "Paciente não encontrado"}), 404
    return jsonify(paciente.to_dict()), 200

@paciente_bp.route("/", methods=["POST"])
def criar_paciente():
    dados = request.get_json()
    response, status = PacienteModel.criar(dados)
    return jsonify(response), status

@paciente_bp.route("/<int:id_paciente>", methods=["PUT"])
def atualizar_paciente(id_paciente):
    dados = request.get_json()
    response, status = PacienteModel.atualizar(id_paciente, dados)
    return jsonify(response), status

@paciente_bp.route("/<int:id_paciente>", methods=["DELETE"])
def deletar_paciente(id_paciente):
    paciente = PacienteModel.query.get(id_paciente)
    if not paciente:
        return jsonify({"mensagem": "Paciente não encontrado"}), 404

    db.session.delete(paciente)
    db.session.commit()
    return jsonify({"mensagem": "Paciente deletado com sucesso"}), 200
