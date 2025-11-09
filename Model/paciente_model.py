from config import db
import re

class Paciente(db.Model):
    __tablename__ = 'pacientes'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    idade = db.Column(db.Integer, nullable=False)
    genero = db.Column(db.String(20))
    telefone = db.Column(db.String(20))
    email = db.Column(db.String(100), nullable=False)
    senha_bash = db.Column(db.String(100), nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'idade': self.idade,
            'genero': self.genero,
            'telefone': self.telefone,
            'email': self.email
        }

    @staticmethod
    def validar_paciente(dados):
        erros = []

        nome = dados.get('nome')
        idade = dados.get('idade')
        genero = dados.get('genero')
        telefone = dados.get('telefone')
        email = dados.get('email')
        senha_bash = dados.get('senha_bash')

        if not nome or len(nome.strip()) < 3:
            erros.append("O nome deve ter pelo menos 3 caracteres.")
        if not isinstance(idade, int) or idade <= 0:
            erros.append("A idade deve ser um número positivo.")
        if genero and genero.lower() not in ['masculino', 'feminino', 'outro']:
            erros.append("O gênero deve ser 'Masculino', 'Feminino' ou 'Outro'.")
        if telefone and (len(telefone) < 8 or len(telefone) > 15):
            erros.append("Telefone deve ter entre 8 e 15 dígitos.")
        if not email or not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email):
            erros.append("E-mail inválido. Forneça um e-mail válido no formato exemplo@dominio.com")
        if not senha_bash or len(senha_bash) < 6:
            erros.append("A senha deve ter pelo menos 6 caracteres.")

        return erros

    @staticmethod
    def listar_pacientes():
        pacientes = Paciente.query.all()
        return [p.to_dict() for p in pacientes], 200

    @staticmethod
    def obter_paciente(id):
        paciente = Paciente.query.get(id)
        if not paciente:
            return {'erro': 'Paciente não encontrado'}, 404
        return paciente.to_dict(), 200

    @staticmethod
    def adicionar_paciente(dados):
        erros = Paciente.validar_paciente(dados)
        if erros:
            return {'erros': erros}, 400

        novo = Paciente(
            nome=dados['nome'],
            idade=dados['idade'],
            genero=dados.get('genero'),
            telefone=dados.get('telefone'),
            email=dados['email'],
            senha_bash=dados['senha_bash']
        )
        db.session.add(novo)
        db.session.commit()
        return {'mensagem': 'Paciente criado com sucesso', 'paciente': novo.to_dict()}, 201

    @staticmethod
    def atualizar_paciente(id, dados):
        paciente = Paciente.query.get(id)
        if not paciente:
            return {'erro': 'Paciente não encontrado'}, 404

        paciente.nome = dados.get('nome', paciente.nome)
        paciente.idade = dados.get('idade', paciente.idade)
        paciente.genero = dados.get('genero', paciente.genero)
        paciente.telefone = dados.get('telefone', paciente.telefone)
        paciente.email = dados.get('email', paciente.email)
        paciente.senha_bash = dados.get('senha_bash', paciente.senha_bash)

        erros = Paciente.validar_paciente({
            **paciente.to_dict(),
            'senha_bash': paciente.senha_bash
        })
        if erros:
            return {'erros': erros}, 400

        db.session.commit()
        return {'mensagem': 'Paciente atualizado com sucesso', 'paciente': paciente.to_dict()}, 200

    @staticmethod
    def deletar_paciente(id):
        paciente = Paciente.query.get(id)
        if not paciente:
            return {'erro': 'Paciente não encontrado'}, 404

        db.session.delete(paciente)
        db.session.commit()
        return {'mensagem': 'Paciente deletado com sucesso'}, 200
