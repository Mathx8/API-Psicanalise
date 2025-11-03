from flask_restx import Namespace, Resource, fields
from Model.psicologo_model import Psicologo
from Model.terapia_model import Terapia

psicologo_ns = Namespace("Psicologo", description="Operações relacionadas aos psicologos")

psicologo_model = psicologo_ns.model("Psicologo", {
    "crp": fields.String(required=True, description="CRP do Psicologo", exemple = "Masculino"),
    "nome": fields.String(required=True, description="Nome do Psicologo", exemple = "Tiago"),
    "idade": fields.Integer(required=True, description="Idade do Psicologo", exemple = 20),
    "telefone": fields.String(required=True, description="Telefone do Psicologo", exemple = "1140028922"),
    "especializacao": fields.String(required=True, description="Especialização do Psicologo", exemple = "Psicologia Clínica"),
    "email": fields.String(required=True, description="E-mail do Psicologo", example="tiago@gmail.com"),
    "senha": fields.String(required=True, description="Senha do Psicologo", example="******")
})

psicologo_model_output = psicologo_ns.model("PsicologoOutput", {
    "id": fields.Integer(description="ID do Psicologo", example=1),
    "crp": fields.String(description="CRP do Psicologo", exemple = "12345-SP"),
    "nome": fields.String(description="Nome do Psicologo", exemple = "Tiago"),
    "idade": fields.Integer(description="Idade do Psicologo", exemple = 20),
    "telefone": fields.String(description="Telefone do Psicologo", exemple = "1140028922"),
    "especializacao": fields.String(description="Especialização do Psicologo", exemple = "Psicologia Clínica"),
    "email": fields.String( description="E-mail do Psicologo", example="tiago@gmail.com")
})

paciente_model_output = psicologo_ns.model("PacienteOutput", {
    "id": fields.Integer(description="ID do paciente", example=1),
    "nome": fields.String(description="Nome do paciente", example="João Silva"),
    "idade": fields.Integer(description="Idade do paciente", example=30),
    "genero": fields.String(description="Gênero do paciente", example="Masculino"),
    "telefone": fields.String(description="Telefone do paciente", example="11987654321"),
    "email": fields.String(description="E-mail do paciente", example="joao@gmail.com"),
})

erro_model = psicologo_ns.model("Erro", {
    "erro": fields.String(example="Psicologo não encontrado")
})

@psicologo_ns.route('/')
class SalaResource(Resource):
    @psicologo_ns.marshal_list_with(psicologo_model_output)
    def get(self):
        """Listar todos os psicologos"""
        return Psicologo.listar_psicologos()

    @psicologo_ns.expect(psicologo_model)
    @psicologo_ns.response(201, "Psicologo criado com sucesso", model=psicologo_model_output)
    @psicologo_ns.response(400, "Dados inválidos", model=erro_model)
    def post(self):
        """Criar um novo psicologo"""
        dados = psicologo_ns.payload
        resultado, status_code = Psicologo.adicionar_psicologo(dados)
        return resultado, status_code
    
@psicologo_ns.route('/<int:id_psicologo>')
class PsicologoIdResource(Resource):
    @psicologo_ns.response(200, "Psicologo encontrado", psicologo_model_output)
    @psicologo_ns.response(404, "Psicologo não encontrado", model=erro_model)
    def get(self, id_psicologo):
        """Obter um psicologo pelo ID"""
        resultado, status_code = Psicologo.obter_psicologo(id_psicologo)
        return resultado, status_code

    @psicologo_ns.expect(psicologo_model)
    @psicologo_ns.response(200, "Psicologo atualizado com sucesso", psicologo_model_output)
    @psicologo_ns.response(400, "Dados inválidos", model=erro_model)
    @psicologo_ns.response(404, "Psicologo não encontrado", model=erro_model)
    def put(self, id_psicologo):
        """Atualizar um psicologo pelo ID"""
        dados = psicologo_ns.payload
        dados['id'] = id_psicologo
        resultado, status_code = Psicologo.atualizar_psicologo(dados)
        return resultado, status_code

    @psicologo_ns.response(200, "Psicologo deletado com sucesso")
    @psicologo_ns.response(404, "Psicologo não encontrado", model=erro_model)
    def delete(self, id_psicologo):
        """Excluir um psicologo pelo ID"""
        resultado, status_code = Psicologo.deletar_psicologo(id_psicologo)
        return resultado, status_code
    

@psicologo_ns.route('/<int:id_psicologo>/pacientes')
class PacientesPorPsicologoResource(Resource):
    @psicologo_ns.marshal_list_with(paciente_model_output)
    @psicologo_ns.response(200, "Pacientes encontrados")
    @psicologo_ns.response(404, "Nenhum paciente encontrado", model=erro_model)
    def get(self, id_psicologo):
        """Listar todos os pacientes atendidos por um psicólogo"""
        resultado, status_code = Terapia.listar_pacientes_por_psicologo(id_psicologo)
        return resultado, status_code