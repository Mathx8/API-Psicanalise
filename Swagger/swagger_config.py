from . import api

from Swagger.namespace.sala_namespace import sala_ns
from Swagger.namespace.paciente_namespace import paciente_ns
from Swagger.namespace.psicologo_namespace import psicologo_ns

def configure_swagger(app):
    api.init_app(app)

    api.add_namespace(sala_ns, path="/salas")
    api.add_namespace(paciente_ns, path="/pacientes")
    api.add_namespace(psicologo_ns, path="/psicologos")
    
    api.mask_swagger = False