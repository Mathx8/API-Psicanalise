from flask_restx import Namespace, Resource, fields
from Model.laudo_model import Laudo

laudo_ns = Namespace("Laudo", description="Operações relacionadas a laudos de terapia")

laudo_model = laudo_ns.model("Laudo", {
    "id_terapia": fields.Integer(required=True, description="ID da terapia relacionada", example=1),
    "texto": fields.String(required=True, description="Descrição do laudo (mínimo 3 caracteres)", example="Paciente apresentou evolução positiva durante a sessão."),
})

laudo_output_model = laudo_ns.model("LaudoOutput", {
    "id": fields.Integer(description="ID do laudo", example=5),
    "id_terapia": fields.Integer(description="ID da terapia relacionada", example=1),
    "texto": fields.String(description="Descrição do laudo", example="Paciente apresentou evolução positiva durante a sessão."),
})

erro_model = laudo_ns.model("Erro", {
    "erro": fields.String(example="Laudo não encontrado"),
})

@laudo_ns.route('/')
class LaudoListResource(Resource):
    @laudo_ns.marshal_list_with(laudo_output_model)
    def get(self):
        """Listar todos os laudos"""
        return Laudo.listar_laudos()[0]

    @laudo_ns.expect(laudo_model)
    @laudo_ns.response(201, "Laudo criado com sucesso", model=laudo_output_model)
    @laudo_ns.response(400, "Dados inválidos", model=erro_model)
    def post(self):
        """Criar um novo laudo"""
        dados = laudo_ns.payload
        resultado, status_code = Laudo.adicionar_laudo(dados)
        return resultado, status_code

@laudo_ns.route('/<int:id_laudo>')
class LaudoResource(Resource):
    @laudo_ns.response(200, "Laudo encontrado", laudo_output_model)
    @laudo_ns.response(404, "Laudo não encontrado", model=erro_model)
    def get(self, id_laudo):
        """Obter um laudo pelo ID"""
        resultado, status_code = Laudo.obter_laudo(id_laudo)
        return resultado, status_code

    @laudo_ns.expect(laudo_model)
    @laudo_ns.response(200, "Laudo atualizado com sucesso", laudo_output_model)
    @laudo_ns.response(400, "Dados inválidos", model=erro_model)
    @laudo_ns.response(404, "Laudo não encontrado", model=erro_model)
    def put(self, id_laudo):
        """Atualizar um laudo pelo ID"""
        dados = laudo_ns.payload
        dados['id'] = id_laudo
        resultado, status_code = Laudo.atualizar_laudo(dados)
        return resultado, status_code

    @laudo_ns.response(200, "Laudo deletado com sucesso")
    @laudo_ns.response(404, "Laudo não encontrado", model=erro_model)
    def delete(self, id_laudo):
        """Excluir um laudo pelo ID"""
        resultado, status_code = Laudo.deletar_laudo(id_laudo)
        return resultado, status_code