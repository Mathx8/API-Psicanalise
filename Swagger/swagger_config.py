from . import api

from Swagger.namespace.sala_namespace import sala_ns
from Swagger.namespace.paciente_namespace import paciente_ns
from Swagger.namespace.psicologo_namespace import psicologo_ns
from Swagger.namespace.disponibilidade_namespace import disponibilidade_ns
from Swagger.namespace.terapia_namespace import terapia_ns
from Swagger.namespace.laudo_namespace import laudo_ns

def configure_swagger(app):
    api.init_app(app)

    api.add_namespace(psicologo_ns, path="/psicologos")
    api.add_namespace(paciente_ns, path="/pacientes")
    api.add_namespace(sala_ns, path="/salas")
    api.add_namespace(disponibilidade_ns, path="/disponibilidades")
    api.add_namespace(terapia_ns, path="/terapias")
    api.add_namespace(laudo_ns, path="/laudos")
    
    api.mask_swagger = False