from flask_restx import Namespace, Resource, fields
from Model.paciente_model import Paciente

paciente_ns = Namespace("Paciente", description="Operações relacionadas aos pacientes")

paciente_model = paciente_ns.model("Paciente", {
    "nome": fields.String(required=True, description="Nome do Paciente", exemple = "Tiago"),
    "idade": fields.Integer(required=True, description="Idade do Paciente", exemple = 20),
    "genero": fields.String(required=True, description="Gênero do paciente", exemple = "Masculino"),
    "telefone": fields.String(required=True, description="Telefone do paciente", exemple = "1140028922"),
    "email": fields.String(required=True, description="E-mail do paciente", example="tiago@gmail.com"),
    "senha": fields.String(required=True, description="Senha do paciente", example="******")
})

paciente_model_output = paciente_ns.model("PacienteOutput", {
    "id": fields.Integer(description="ID do Paciente", example=1),
    "nome": fields.String(description="Nome do Paciente", exemple = "Tiago"),
    "idade": fields.Integer(description="Idade do Paciente", exemple = 20),
    "genero": fields.String(description="Gênero do paciente", exemple = "Masculino"),
    "telefone": fields.String(description="Telefone do paciente", exemple = "1140028922"),
    "email": fields.String(description="E-mail do paciente", example="tiago@gmail.com"),
})

erro_model = paciente_ns.model("Erro", {
    "erro": fields.String(example="Paciente não encontrado")
})

@paciente_ns.route('/')
class SalaResource(Resource):
    @paciente_ns.marshal_list_with(paciente_model_output)
    def get(self):
        """Listar todos os pacientes"""
        return Paciente.listar_pacientes()

    @paciente_ns.expect(paciente_model)
    @paciente_ns.response(201, "Paciente criado com sucesso", model=paciente_model_output)
    @paciente_ns.response(400, "Dados inválidos", model=erro_model)
    def post(self):
        """Criar um novo paciente"""
        dados = paciente_ns.payload
        resultado, status_code = Paciente.adicionar_paciente(dados)
        return resultado, status_code
    
@paciente_ns.route('/<int:id_paciente>')
class PacienteIdResource(Resource):
    @paciente_ns.response(200, "Paciente encontrado", paciente_model_output)
    @paciente_ns.response(404, "Paciente não encontrado", model=erro_model)
    def get(self, id_paciente):
        """Obter um paciente pelo ID"""
        resultado, status_code = Paciente.obter_paciente(id_paciente)
        return resultado, status_code

    @paciente_ns.expect(paciente_model)
    @paciente_ns.response(200, "Paciente atualizado com sucesso", paciente_model_output)
    @paciente_ns.response(400, "Dados inválidos", model=erro_model)
    @paciente_ns.response(404, "Paciente não encontrado", model=erro_model)
    def put(self, id_paciente):
        """Atualizar um paciente pelo ID"""
        dados = paciente_ns.payload
        dados['id'] = id_paciente
        resultado, status_code = Paciente.atualizar_paciente(dados)
        return resultado, status_code

    @paciente_ns.response(200, "Paciente deletado com sucesso")
    @paciente_ns.response(404, "Paciente não encontrado", model=erro_model)
    def delete(self, id_paciente):
        """Excluir um paciente pelo ID"""
        resultado, status_code = Paciente.deletar_paciente(id_paciente)
        return resultado, status_code