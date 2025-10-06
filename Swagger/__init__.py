from flask_restx import Api

api = Api(
    version="1.0",
    title="API de Psicanalise",
    description="Documentação da API para Psicologo e Pacientes",
    doc="/",
    mask_swagger=False,
)