from config import db
from datetime import datetime, timedelta

class Terapia(db.Model):
    __tablename__ = 'terapia'

    id = db.Column(db.Integer, primary_key=True)
    id_psicologo = db.Column(db.Integer, db.ForeignKey('psicologo.id', ondelete='CASCADE'), nullable=False)
    id_paciente = db.Column(db.Integer, db.ForeignKey('pacientes.id', ondelete='CASCADE'), nullable=False)
    id_sala = db.Column(db.Integer, db.ForeignKey('sala.id', ondelete='SET NULL'), nullable=True)
    data = db.Column(db.DateTime, nullable=False)
    duracao = db.Column(db.Time, nullable=True)
    numero_sessao = db.Column(db.Integer, nullable=False)

    psicologo = db.relationship('Psicologo', backref=db.backref('terapias', lazy=True, cascade="all, delete"))
    paciente = db.relationship('Paciente', backref=db.backref('terapias', lazy=True, cascade="all, delete"))
    sala = db.relationship('Sala', backref=db.backref('terapias', lazy=True))

    def to_dict(self):
        return {
            'id': self.id,
            'id_psicologo': self.id_psicologo,
            'nome_psicologo': self.psicologo.nome if self.psicologo else None,
            'id_paciente': self.id_paciente,
            'nome_paciente': self.paciente.nome if self.paciente else None,
            'id_sala': self.id_sala,
            'nome_sala': self.sala.nome if self.sala else None,
            'data': self.data,
            'duracao': self.duracao,
            'numero_sessao': self.numero_sessao
        }
    
    @staticmethod
    def validar_terapia(dados):
        erros = []

        id_psicologo = dados.get('id_psicologo')
        id_paciente = dados.get('id_paciente')
        data = dados.get('data')
        duracao = dados.get('duracao')
        numero_sessao = dados.get('numero_sessao')

        if not id_psicologo:
            erros.append('O campo id_psicologo é obrigatório.')

        if not id_paciente:
            erros.append('O campo id_paciente é obrigatório.')

        if not data:
            erros.append('A data da terapia é obrigatória.')
        else:
            try:
                datetime.strptime(dados.get('data'), "%Y-%m-%d %H:%M:%S")
            except ValueError:
                erros.append('Formato de data inválido. Use o formato YYYY-MM-DD HH:MM:SS.')

        if duracao:
            try:
                datetime.strptime(duracao, "%H:%M:%S")
            except ValueError:
                erros.append('Formato de duração inválido. Use HH:MM:SS.')

        if not isinstance(numero_sessao, int) or numero_sessao <= 0:
            erros.append('O número da sessão deve ser um inteiro positivo.')

        return erros

    @staticmethod
    def listar_terapias():
        terapias = Terapia.query.all()
        return [terapia.to_dict() for terapia in terapias], 200

    @staticmethod
    def obter_terapia(id):
        terapia = Terapia.query.get(id)
        if not terapia:
            return {'erro': 'Terapia não encontrada'}, 404
        return terapia.to_dict(), 200

    @staticmethod
    def adicionar_terapia(dados):
        erros = Terapia.validar_terapia(dados)
        if erros:
            return {'erros': erros}, 400

        duracao_str = dados.get('duracao')
        nova = Terapia(
            id_psicologo=dados.get('id_psicologo'),
            id_paciente=dados.get('id_paciente'),
            id_sala=dados.get('id_sala'),
            data=datetime.strptime(dados.get('data'), "%Y-%m-%d %H:%M:%S"),
            duracao=datetime.strptime(duracao_str, "%H:%M:%S").time() if duracao_str else None,
            numero_sessao=dados.get('numero_sessao')
        )

        db.session.add(nova)
        db.session.commit()
        return {'mensagem': 'Terapia criada com sucesso', 'Terapia': nova.to_dict()}, 201

    @staticmethod
    def atualizar_terapia(dados):
        terapia = Terapia.query.get(dados.get('id'))
        if not terapia:
            return {'erro': 'Terapia não encontrada'}, 404

        erros = Terapia.validar_terapia(dados)
        if erros:
            return {'erros': erros}, 400

        terapia.id_psicologo = dados.get('id_psicologo', terapia.id_psicologo)
        terapia.id_paciente = dados.get('id_paciente', terapia.id_paciente)
        terapia.id_sala = dados.get('id_sala', terapia.id_sala)
        terapia.data = datetime.strptime(dados.get('data'), "%Y-%m-%d %H:%M:%S")

        duracao_str = dados.get('duracao')
        terapia.duracao = (
            datetime.strptime(duracao_str, "%H:%M:%S").time()
            if duracao_str else terapia.duracao
        )

        terapia.numero_sessao = dados.get('numero_sessao', terapia.numero_sessao)

        db.session.commit()
        return {'mensagem': 'Terapia atualizada com sucesso', 'Terapia': terapia.to_dict()}, 200

    @staticmethod
    def deletar_terapia(id):
        terapia = Terapia.query.get(id)
        if not terapia:
            return {'erro': 'Terapia não encontrada'}, 404

        db.session.delete(terapia)
        db.session.commit()
        return {'mensagem': 'Terapia deletada com sucesso'}, 200

    @staticmethod
    def listar_por_dia(data_str, psicologo_id=None):
        try:
            data = datetime.strptime(data_str, "%Y-%m-%d").date()
        except ValueError:
            return {'erro': 'Formato inválido. Use YYYY-MM-DD.'}, 400

        query = Terapia.query.filter(db.func.date(Terapia.data) == data)

        if psicologo_id:
            query = query.filter(Terapia.id_psicologo == psicologo_id)

        terapias = query.all()
        return [terapia.to_dict() for terapia in terapias], 200

    @staticmethod
    def listar_por_semana(inicio_str, fim_str, psicologo_id=None):
        try:
            inicio = datetime.strptime(inicio_str, "%Y-%m-%d")
            fim = datetime.strptime(fim_str, "%Y-%m-%d") + timedelta(days=1)
        except ValueError:
            return {'erro': 'Formato inválido. Use YYYY-MM-DD.'}, 400

        query = Terapia.query.filter(
            Terapia.data >= inicio,
            Terapia.data < fim
        )

        if psicologo_id:
            query = query.filter(Terapia.id_psicologo == psicologo_id)

        terapias = query.all()
        return [terapia.to_dict() for terapia in terapias], 200