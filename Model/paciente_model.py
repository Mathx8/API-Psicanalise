from database import db

class PacienteModel(db.Model):
    __tablename__ = 'pacientes'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    senha_bash = db.Column(db.String(100), nullable=False)
    telefone = db.Column(db.String(20), nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "email": self.email,
            "telefone": self.telefone
        }

    # --- 🔍 Validação de dados ---
    @staticmethod
    def validar_dados(dados):
        """Valida se todos os campos obrigatórios estão presentes e corretos."""
        campos_obrigatorios = ['nome', 'email', 'senha_bash', 'telefone']

        for campo in campos_obrigatorios:
            if campo not in dados or not dados[campo]:
                return False, f"Campo obrigatório ausente ou vazio: '{campo}'"

        # Exemplo de validações simples
        if "@" not in dados['email']:
            return False, "E-mail inválido."

        if len(dados['senha_bash']) < 6:
            return False, "A senha deve ter pelo menos 6 caracteres."

        if not dados['telefone'].isdigit():
            return False, "O telefone deve conter apenas números."

        return True, "OK"

    # --- 🔧 Métodos de criação/atualização seguros ---
    @classmethod
    def criar(cls, dados):
        valido, msg = cls.validar_dados(dados)
        if not valido:
            return {"mensagem": msg}, 400

        try:
            novo = cls(
                nome=dados['nome'],
                email=dados['email'],
                senha_bash=dados['senha_bash'],
                telefone=dados['telefone']
            )
            db.session.add(novo)
            db.session.commit()
            return novo.to_dict(), 201
        except Exception as e:
            db.session.rollback()
            return {"mensagem": f"Erro ao salvar no banco de dados: {str(e)}"}, 500

    @classmethod
    def atualizar(cls, id_paciente, dados):
        paciente = cls.query.get(id_paciente)
        if not paciente:
            return {"mensagem": "Paciente não encontrado"}, 404

        # Atualiza somente campos enviados
        for campo in ['nome', 'email', 'senha_bash', 'telefone']:
            if campo in dados and dados[campo]:
                setattr(paciente, campo, dados[campo])

        # Valida novamente após atualização
        valido, msg = cls.validar_dados(paciente.to_dict() | {"senha_bash": paciente.senha_bash})
        if not valido:
            return {"mensagem": msg}, 400

        try:
            db.session.commit()
            return paciente.to_dict(), 200
        except Exception as e:
            db.session.rollback()
            return {"mensagem": f"Erro ao atualizar paciente: {str(e)}"}, 500
