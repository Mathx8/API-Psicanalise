from config import db
import re

class Psicologo(db.Model):
    __tablename__ = 'psicologo'

    id = db.Column(db.Integer, primary_key=True)
    crp = db.Column(db.String(100), nullable=False)
    nome = db.Column(db.String(100), nullable=False)
    idade = db.Column(db.Integer, nullable=False)
    email = db.Column(db.String(100), nullable=False)
    senha_bash = db.Column(db.String(100), nullable=False)
    telefone = db.Column(db.String(100), nullable=False)
    especializacao = db.Column(db.String(100), nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'crp': self.crp,
            'nome': self.nome,
            'idade': self.idade,
            'email': self.email,
            'telefone': self.telefone,
            'especializacao': self.especializacao
        }

    # =================== FUNÇÕES DE NEGÓCIO ===================

    @staticmethod
    def validar_psicologo(dados):
        erros = []

        crp = dados.get('crp')
        nome = dados.get('nome')
        idade = dados.get('idade')
        email = dados.get('email')
        senha_bash = dados.get('senha_bash')
        telefone = dados.get('telefone')
        especializacao = dados.get('especializacao')

        if not crp or len(crp.strip()) < 3:
            erros.append('O CRP deve ter pelo menos 3 caracteres.')

        if not nome or len(nome.strip()) < 3:
            erros.append('O nome deve ter pelo menos 3 caracteres.')

        if not isinstance(idade, int) or idade <= 0:
            erros.append("A idade deve ser um número positivo.")

        if not email or not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email):
            erros.append('E-mail inválido. Forneça um e-mail válido no formato exemplo@dominio.com')

        if not senha_bash or len(senha_bash) < 6:
            erros.append("A senha deve ter pelo menos 6 caracteres.")

        if telefone and (len(telefone) < 8 or len(telefone) > 15):
            erros.append("Telefone deve ter entre 8 e 15 dígitos.")

        if not especializacao or len(especializacao.strip()) < 3:
            erros.append("Especialização deve ter pelo menos 3 caracteres.")

        return erros

    @staticmethod
    def listar_psicologos():
        psicologos = Psicologo.query.all()
        return [psicologo.to_dict() for psicologo in psicologos], 200

    @staticmethod
    def obter_psicologo(id):
        psicologo = Psicologo.query.get(id)
        if not psicologo:
            return {'erro': 'Psicologo não encontrado'}, 404
        return psicologo.to_dict(), 200

    @staticmethod
    def adicionar_psicologo(dados):
        erros = Psicologo.validar_psicologo(dados)
        if erros:
            return {'erros': erros}, 400

        novo = Psicologo(
            crp=dados.get('crp'),
            nome=dados.get('nome'),
            idade=dados.get('idade'),
            email=dados.get('email'),
            senha_bash=dados.get('senha_bash'),
            telefone=dados.get('telefone'),
            especializacao=dados.get('especializacao')
        )

        db.session.add(novo)
        db.session.commit()
        return {'mensagem': 'Psicologo criado com sucesso', 'Psicologo': novo.to_dict()}, 201

    @staticmethod
    def atualizar_psicologo(dados):
        psicologo = Psicologo.query.get(dados.get('id'))
        if not psicologo:
            return {'erro': 'Psicologo não encontrado'}, 404

        psicologo.crp = dados.get('crp', psicologo.crp)
        psicologo.nome = dados.get('nome', psicologo.nome)
        psicologo.idade = dados.get('idade', psicologo.idade)
        psicologo.email = dados.get('email', psicologo.email)
        psicologo.senha_bash = dados.get('senha_bash', psicologo.senha_bash)
        psicologo.telefone = dados.get('telefone', psicologo.telefone)
        psicologo.especializacao = dados.get('especializacao', psicologo.especializacao)

        erros = Psicologo.validar_psicologo(psicologo.to_dict())
        if erros:
            return {'erros': erros}, 400

        db.session.commit()
        return {'mensagem': 'Psicologo atualizado com sucesso', 'Psicologo': psicologo.to_dict()}, 200

    @staticmethod
    def deletar_psicologo(id):
        psicologo = Psicologo.query.get(id)
        if not psicologo:
            return {'erro': 'Psicologo não encontrado'}, 404

        db.session.delete(psicologo)
        db.session.commit()
        return {'mensagem': 'Psicologo deletado com sucesso'}, 200
