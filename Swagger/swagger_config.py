from . import api

from Swagger.namespace.sala_namespace import sala_ns

def configure_swagger(app):
    api.init_app(app)

    api.add_namespace(sala_ns, path="/salas")
    
    api.mask_swagger = False