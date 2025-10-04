from config import db

class Paciente(db.Model):
    __tablename__ = 'pacientes'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    idade = db.Column(db.Integer, nullable=False)
    genero = db.Column(db.String(20))
    telefone = db.Column(db.String(20))

    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'idade': self.idade,
            'genero': self.genero,
            'telefone': self.telefone
        }

# =================== FUNÇÕES DE NEGÓCIO ===================

def validar_paciente(dados):
    erros = []

    nome = dados.get('nome')
    idade = dados.get('idade')
    genero = dados.get('genero')
    telefone = dados.get('telefone')

    if not nome or len(nome.strip()) < 3:
        erros.append("O nome deve ter pelo menos 3 caracteres.")

    if not isinstance(idade, int) or idade <= 0:
        erros.append("A idade deve ser um número positivo.")

    if genero and genero.lower() not in ['masculino', 'feminino', 'outro']:
        erros.append("O gênero deve ser 'Masculino', 'Feminino' ou 'Outro'.")

    if telefone and (len(telefone) < 8 or len(telefone) > 15):
        erros.append("Telefone deve ter entre 8 e 15 dígitos.")

    return erros


def listar_pacientes():
    pacientes = Paciente.query.all()
    return [p.to_dict() for p in pacientes], 200


def obter_paciente(id):
    paciente = Paciente.query.get(id)
    if not paciente:
        return {'erro': 'Paciente não encontrado'}, 404
    return paciente.to_dict(), 200


def adicionar_paciente(dados):
    erros = validar_paciente(dados)
    if erros:
        return {'erros': erros}, 400

    novo = Paciente(
        nome=dados['nome'],
        idade=dados['idade'],
        genero=dados.get('genero'),
        telefone=dados.get('telefone')
    )

    db.session.add(novo)
    db.session.commit()
    return {'mensagem': 'Paciente criado com sucesso', 'paciente': novo.to_dict()}, 201


def atualizar_paciente(id, dados):
    paciente = Paciente.query.get(id)
    if not paciente:
        return {'erro': 'Paciente não encontrado'}, 404

    paciente.nome = dados.get('nome', paciente.nome)
    paciente.idade = dados.get('idade', paciente.idade)
    paciente.genero = dados.get('genero', paciente.genero)
    paciente.telefone = dados.get('telefone', paciente.telefone)

    erros = validar_paciente(paciente.to_dict())
    if erros:
        return {'erros': erros}, 400

    db.session.commit()
    return {'mensagem': 'Paciente atualizado com sucesso', 'paciente': paciente.to_dict()}, 200


def deletar_paciente(id):
    paciente = Paciente.query.get(id)
    if not paciente:
        return {'erro': 'Paciente não encontrado'}, 404

    db.session.delete(paciente)
    db.session.commit()
    return {'mensagem': 'Paciente deletado com sucesso'}, 200
