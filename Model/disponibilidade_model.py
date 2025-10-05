from config import db
from datetime import datetime, timedelta

class Disponibilidade(db.Model):
    __tablename__ = 'disponibilidade'

    id = db.Column(db.Integer, primary_key=True)
    id_psicologo = db.Column(db.Integer, db.ForeignKey('psicologo.id', ondelete='CASCADE'), nullable=False)
    id_sala = db.Column(db.Integer, db.ForeignKey('sala.id', ondelete='SET NULL'), nullable=True)
    data = db.Column(db.DateTime, nullable=False)
    horario_inicial = db.Column(db.Time, nullable=False)
    horario_final = db.Column(db.Time, nullable=False)

    psicologo = db.relationship('Psicologo', backref=db.backref('disponibilidades', lazy=True, cascade="all, delete"))
    sala = db.relationship('Sala', backref=db.backref('disponibilidades', lazy=True))

    def to_dict(self):
        return {
            'id': self.id,
            'id_psicologo': self.id_psicologo,
            'nome_psicologo': self.psicologo.nome if self.psicologo else None,
            'id_sala': self.id_sala,
            'nome_sala': self.sala.nome if self.sala else None,
            'data': self.data.isoformat() if self.data else None,
            'horario_inicial': self.horario_inicial.strftime('%H:%M') if self.horario_inicial else None,
            'horario_final': self.horario_final.strftime('%H:%M') if self.horario_final else None
        }
    
    @staticmethod
    def validar_disponibilidade(dados):
        erros = []

        id_psicologo = dados.get('id_psicologo')
        data = dados.get('data')
        horario_inicial = dados.get('horario_inicial')
        horario_final = dados.get('horario_final')

        if not id_psicologo:
            erros.append("O campo 'id_psicologo' é obrigatório.")

        if not data:
            erros.append("O campo 'data' é obrigatório.")
        else:
            try:
                datetime.fromisoformat(data)
            except ValueError:
                erros.append("Formato de data inválido. Use o formato YYYY-MM-DDTHH:MM:SS.")

        if not horario_inicial or not horario_final:
            erros.append("Horários inicial e final são obrigatórios.")
        else:
            try:
                h_inicial = datetime.strptime(horario_inicial, "%H:%M").time()
                h_final = datetime.strptime(horario_final, "%H:%M").time()
                if h_inicial >= h_final:
                    erros.append("O horário inicial deve ser menor que o horário final.")
            except ValueError:
                erros.append("Formato de horário inválido. Use HH:MM.")

        return erros

    @staticmethod
    def listar_disponibilidades():
        disponibilidades = Disponibilidade.query.all()
        return [disponibilidade.to_dict() for disponibilidade in disponibilidades], 200
    
    @staticmethod
    def obter_disponibilidade(id):
        disponibilidade = Disponibilidade.query.get(id)
        if not disponibilidade:
            return {'erro': 'Disponibilidade não encontrada'}, 404
        return disponibilidade.to_dict(), 200
    
    @staticmethod
    def adicionar_disponibilidade(dados):
        erros = Disponibilidade.validar_disponibilidade(dados)
        if erros:
            return {'erros': erros}, 400

        nova = Disponibilidade(
            id_psicologo=dados.get('id_psicologo'),
            id_sala=dados.get('id_sala'),
            data=datetime.fromisoformat(dados.get('data')),
            horario_inicial=datetime.strptime(dados.get('horario_inicial'), "%H:%M").time(),
            horario_final=datetime.strptime(dados.get('horario_final'), "%H:%M").time()
        )

        db.session.add(nova)
        db.session.commit()
        return {'mensagem': 'Disponibilidade criada com sucesso', 'Disponibilidade': nova.to_dict()}, 201

    @staticmethod
    def atualizar_disponibilidade(dados):
        disponibilidade = Disponibilidade.query.get(dados.get('id'))
        if not disponibilidade:
            return {'erro': 'Disponibilidade não encontrada'}, 404

        disponibilidade.id_psicologo = dados.get('id_psicologo', disponibilidade.id_psicologo)
        disponibilidade.id_sala = dados.get('id_sala', disponibilidade.id_sala)

        if 'data' in dados:
            try:
                disponibilidade.data = datetime.fromisoformat(dados.get('data'))
            except ValueError:
                return {'erro': 'Formato de data inválido. Use o formato YYYY-MM-DDTHH:MM:SS'}, 400

        if 'horario_inicial' in dados:
            try:
                disponibilidade.horario_inicial = datetime.strptime(dados.get('horario_inicial'), "%H:%M").time()
            except ValueError:
                return {'erro': 'Formato de horário inicial inválido. Use HH:MM'}, 400

        if 'horario_final' in dados:
            try:
                disponibilidade.horario_final = datetime.strptime(dados.get('horario_final'), "%H:%M").time()
            except ValueError:
                return {'erro': 'Formato de horário final inválido. Use HH:MM'}, 400

        erros = Disponibilidade.validar_disponibilidade({
            'id_psicologo': disponibilidade.id_psicologo,
            'data': disponibilidade.data.isoformat(),
            'horario_inicial': disponibilidade.horario_inicial.strftime('%H:%M'),
            'horario_final': disponibilidade.horario_final.strftime('%H:%M')
        })
        if erros:
            return {'erros': erros}, 400

        db.session.commit()
        return {'mensagem': 'Disponibilidade atualizada com sucesso', 'Disponibilidade': disponibilidade.to_dict()}, 200

    @staticmethod
    def deletar_disponibilidade(id):
        disponibilidade = Disponibilidade.query.get(id)
        if not disponibilidade:
            return {'erro': 'Disponibilidade não encontrada'}, 404

        db.session.delete(disponibilidade)
        db.session.commit()
        return {'mensagem': 'Disponibilidade deletada com sucesso'}, 200
    
    @staticmethod
    def listar_por_dia(data_str):
        try:
            data = datetime.strptime(data_str, "%Y-%m-%d").date()
        except ValueError:
            return {'erro': 'Formato de data inválido. Use YYYY-MM-DD.'}, 400

        disponibilidades = Disponibilidade.query.filter(
            db.func.date(Disponibilidade.data) == data
        ).all()

        return [disponibilidade.to_dict() for disponibilidade in disponibilidades], 200

    @staticmethod
    def listar_por_semana(inicio_str, fim_str):
        try:
            inicio = datetime.strptime(inicio_str, "%Y-%m-%d")
            fim = datetime.strptime(fim_str, "%Y-%m-%d") + timedelta(days=1)
        except ValueError:
            return {'erro': 'Formato inválido. Use YYYY-MM-DD.'}, 400

        disponibilidades = Disponibilidade.query.filter(
            Disponibilidade.data >= inicio,
            Disponibilidade.data < fim
        ).all()

        return [disponibilidade.to_dict() for disponibilidade in disponibilidades], 200