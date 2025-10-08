from flask_restx import Namespace, Resource, fields
from Model.disponibilidade_model import Disponibilidade

disponibilidade_ns = Namespace("Disponibilidade", description="Operações relacionadas à disponibilidade dos psicólogos")

disponibilidade_model = disponibilidade_ns.model("Disponibilidade", {
    "id_psicologo": fields.Integer(required=True, description="ID do psicólogo", example=1),
    "id_sala": fields.Integer(required=False, description="ID da sala", example=2),
    "data": fields.String(required=True, description="Data da disponibilidade (YYYY-MM-DD)", example="2025-10-10"),
    "horario_inicial": fields.String(required=True, description="Horário de início (HH:MM)", example="09:00"),
    "horario_final": fields.String(required=True, description="Horário de término (HH:MM)", example="12:00"),
})

disponibilidade_output_model = disponibilidade_ns.model("DisponibilidadeOutput", {
    "id": fields.Integer(description="ID da disponibilidade", example=1),
    "id_psicologo": fields.Integer(description="ID do psicólogo", example=1),
    "nome_psicologo": fields.String(description="Nome do psicólogo", example="Maria"),
    "id_sala": fields.Integer(description="ID da sala", example=2),
    "nome_sala": fields.String(description="Nome da sala", example="Sala Azul"),
    "data": fields.String(description="Data da disponibilidade (YYYY-MM-DD)", example="2025-10-10"),
    "horario_inicial": fields.String(description="Horário de início (HH:MM)", example="09:00"),
    "horario_final": fields.String(description="Horário de término (HH:MM)", example="12:00"),
})

erro_model = disponibilidade_ns.model("Erro", {
    "erro": fields.String(example="Disponibilidade não encontrada")
})

@disponibilidade_ns.route('/')
class DisponibilidadeListResource(Resource):
    @disponibilidade_ns.marshal_list_with(disponibilidade_output_model)
    def get(self):
        """Listar todas as disponibilidades"""
        return Disponibilidade.listar_disponibilidades()[0]
    
    @disponibilidade_ns.expect(disponibilidade_model)
    @disponibilidade_ns.response(201, "Disponibilidade criada com sucesso", model=disponibilidade_output_model)
    @disponibilidade_ns.response(400, "Dados inválidos", model=erro_model)
    def post(self):
        """Criar uma nova disponibilidade"""
        dados = disponibilidade_ns.payload
        resultado, status_code = Disponibilidade.adicionar_disponibilidade(dados)
        return resultado, status_code

@disponibilidade_ns.route('/<int:id_disponibilidade>')
class DisponibilidadeResource(Resource):
    @disponibilidade_ns.response(200, "Disponibilidade encontrada", disponibilidade_output_model)
    @disponibilidade_ns.response(404, "Disponibilidade não encontrada", model=erro_model)
    def get(self, id_disponibilidade):
        """Obter uma disponibilidade pelo ID"""
        resultado, status_code = Disponibilidade.obter_disponibilidade(id_disponibilidade)
        return resultado, status_code

    @disponibilidade_ns.expect(disponibilidade_model)
    @disponibilidade_ns.response(200, "Disponibilidade atualizada com sucesso", disponibilidade_output_model)
    @disponibilidade_ns.response(400, "Dados inválidos", model=erro_model)
    @disponibilidade_ns.response(404, "Disponibilidade não encontrada", model=erro_model)
    def put(self, id_disponibilidade):
        """Atualizar uma disponibilidade pelo ID"""
        dados = disponibilidade_ns.payload
        dados['id'] = id_disponibilidade
        resultado, status_code = Disponibilidade.atualizar_disponibilidade(dados)
        return resultado, status_code

    @disponibilidade_ns.response(200, "Disponibilidade deletada com sucesso")
    @disponibilidade_ns.response(404, "Disponibilidade não encontrada", model=erro_model)
    def delete(self, id_disponibilidade):
        """Excluir uma disponibilidade pelo ID"""
        resultado, status_code = Disponibilidade.deletar_disponibilidade(id_disponibilidade)
        return resultado, status_code

@disponibilidade_ns.route('/dia/<string:data>')
class DisponibilidadeDiaResource(Resource):
    @disponibilidade_ns.marshal_list_with(disponibilidade_output_model)
    def get(self, data):
        """Listar disponibilidades por dia (YYYY-MM-DD)"""
        resultado, status_code = Disponibilidade.listar_por_dia(data)
        return resultado, status_code

@disponibilidade_ns.route('/semana/<string:inicio>/<string:fim>')
class DisponibilidadeSemanaResource(Resource):
    @disponibilidade_ns.marshal_list_with(disponibilidade_output_model)
    def get(self, inicio, fim):
        """Listar disponibilidades por semana (YYYY-MM-DD)"""
        resultado, status_code = Disponibilidade.listar_por_semana(inicio, fim)
        return resultado, status_code
