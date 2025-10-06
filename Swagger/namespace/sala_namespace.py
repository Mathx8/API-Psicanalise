from flask_restx import Namespace, Resource, fields
from Model.sala_model import Sala

sala_ns = Namespace("Sala", description="Operações relacionadas às salas")

sala_model = sala_ns.model("Sala", {
    "nome": fields.String(required=True, description="Nome da Sala", exemple = "A1"),
    "descricao": fields.String(required=True, description="Descrição da Sala", exemple = "Sala de atendimento principal"),
})

sala_model_output = sala_ns.model("SalaOutput", {
    "id": fields.Integer(description="ID da sala", example=1),
    "nome": fields.String(description="Nome da sala", example="A1"),
    "descricao": fields.String(description="Descrição da sala", example="Sala de atendimento principal"),
})

erro_model = sala_ns.model("Erro", {
    "erro": fields.String(example="Sala não encontrada")
})

@sala_ns.route('/')
class SalaResource(Resource):
    @sala_ns.marshal_list_with(sala_model_output)
    def get(self):
        """Listar todas as salas"""
        return Sala.listar_salas()

    @sala_ns.expect(sala_model)
    @sala_ns.response(201, "Sala criada com sucesso", model=sala_model_output)
    @sala_ns.response(400, "Dados inválidos", model=erro_model)
    def post(self):
        """Criar uma nova sala"""
        dados = sala_ns.payload
        resultado, status_code = Sala.adicionar_sala(dados)
        return resultado, status_code

@sala_ns.route('/<int:id_sala>')
class SalaIdResource(Resource):
    @sala_ns.response(200, "Sala encontrada", sala_model_output)
    @sala_ns.response(404, "Sala não encontrada", model=erro_model)
    def get(self, id_sala):
        """Obter uma sala pelo ID"""
        resultado, status_code = Sala.obter_sala(id_sala)
        return resultado, status_code

    @sala_ns.expect(sala_model)
    @sala_ns.response(200, "Sala atualizada com sucesso", sala_model_output)
    @sala_ns.response(400, "Dados inválidos", model=erro_model)
    @sala_ns.response(404, "Sala não encontrada", model=erro_model)
    def put(self, id_sala):
        """Atualizar uma sala pelo ID"""
        dados = sala_ns.payload
        dados['id'] = id_sala
        resultado, status_code = Sala.atualizar_sala(dados)
        return resultado, status_code

    @sala_ns.response(200, "Sala deletada com sucesso")
    @sala_ns.response(404, "Sala não encontrada", model=erro_model)
    def delete(self, id_sala):
        """Excluir uma sala pelo ID"""
        resultado, status_code = Sala.deletar_sala(id_sala)
        return resultado, status_code