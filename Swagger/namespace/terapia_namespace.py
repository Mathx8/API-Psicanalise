from flask_restx import Namespace, Resource, fields
from Model.terapia_model import Terapia

terapia_ns = Namespace("Terapia", description="Operações relacionadas às sessões de terapia")

terapia_model = terapia_ns.model("Terapia", {
    "id_psicologo": fields.Integer(required=True, description="ID do psicólogo", example=1),
    "id_paciente": fields.Integer(required=True, description="ID do paciente", example=23),
    "id_sala": fields.Integer(required=False, description="ID da sala", example=2),
    "data": fields.String(required=True, description="Data e horário da sessão (YYYY-MM-DD HH:MM)", example="2025-10-10 10:30"),
    "duracao": fields.String(required=False, description="Duração da sessão (HH:MM)", example="01:00"),
    "numero_sessao": fields.Integer(required=True, description="Número da sessão", example=1),
})

terapia_output_model = terapia_ns.model("TerapiaOutput", {
    "id": fields.Integer(description="ID da terapia", example=1),
    "id_psicologo": fields.Integer(description="ID do psicólogo", example=1),
    "nome_psicologo": fields.String(description="Nome do psicólogo", example="Maria"),
    "id_paciente": fields.Integer(description="ID do paciente", example=23),
    "nome_paciente": fields.String(description="Nome do paciente", example="João"),
    "id_sala": fields.Integer(description="ID da sala", example=2),
    "nome_sala": fields.String(description="Nome da sala", example="Sala Azul"),
    "data": fields.String(description="Data e horário da sessão (YYYY-MM-DD HH:MM)", example="2025-10-10 10:30"),
    "duracao": fields.String(description="Duração da sessão (HH:MM)", example="01:00"),
    "numero_sessao": fields.Integer(description="Número da sessão", example=1),
})

erro_model = terapia_ns.model("Erro", {
    "erro": fields.String(example="Terapia não encontrada"),
})

@terapia_ns.route('/')
class TerapiaListResource(Resource):
    @terapia_ns.marshal_list_with(terapia_output_model)
    def get(self):
        """Listar todas as sessões de terapia"""
        return Terapia.listar_terapias()[0]

    @terapia_ns.expect(terapia_model)
    @terapia_ns.response(201, "Terapia criada com sucesso", model=terapia_output_model)
    @terapia_ns.response(400, "Dados inválidos", model=erro_model)
    def post(self):
        """Criar uma nova sessão de terapia"""
        dados = terapia_ns.payload
        resultado, status_code = Terapia.adicionar_terapia(dados)
        return resultado, status_code

@terapia_ns.route('/<int:id_terapia>')
class TerapiaResource(Resource):
    @terapia_ns.response(200, "Terapia encontrada", terapia_output_model)
    @terapia_ns.response(404, "Terapia não encontrada", model=erro_model)
    def get(self, id_terapia):
        """Obter uma terapia pelo ID"""
        resultado, status_code = Terapia.obter_terapia(id_terapia)
        return resultado, status_code

    @terapia_ns.expect(terapia_model)
    @terapia_ns.response(200, "Terapia atualizada com sucesso", terapia_output_model)
    @terapia_ns.response(400, "Dados inválidos", model=erro_model)
    @terapia_ns.response(404, "Terapia não encontrada", model=erro_model)
    def put(self, id_terapia):
        """Atualizar uma terapia pelo ID"""
        dados = terapia_ns.payload
        dados['id'] = id_terapia
        resultado, status_code = Terapia.atualizar_terapia(dados)
        return resultado, status_code

    @terapia_ns.response(200, "Terapia deletada com sucesso")
    @terapia_ns.response(404, "Terapia não encontrada", model=erro_model)
    def delete(self, id_terapia):
        """Excluir uma terapia pelo ID"""
        resultado, status_code = Terapia.deletar_terapia(id_terapia)
        return resultado, status_code

@terapia_ns.route('/dia/<string:data>')
@terapia_ns.route('/dia/<string:data>/<int:psicologo_id>')
class TerapiaDiaResource(Resource):
    @terapia_ns.marshal_list_with(terapia_output_model)
    def get(self, data, psicologo_id=None):
        """Listar terapias por dia (YYYY-MM-DD), opcionalmente filtrando por psicólogo"""
        resultado, status_code = Terapia.listar_por_dia(data, psicologo_id)
        return resultado, status_code

@terapia_ns.route('/semana/<string:inicio>/<string:fim>')
@terapia_ns.route('/semana/<string:inicio>/<string:fim>/<int:psicologo_id>')
class TerapiaSemanaResource(Resource):
    @terapia_ns.marshal_list_with(terapia_output_model)
    def get(self, inicio, fim, psicologo_id=None):
        """Listar terapias por semana (YYYY-MM-DD), opcionalmente filtrando por psicólogo"""
        resultado, status_code = Terapia.listar_por_semana(inicio, fim, psicologo_id)
        return resultado, status_code