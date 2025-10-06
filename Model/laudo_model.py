from config import db

class Laudo(db.Model):
    __tablename__ = 'laudo'

    id = db.Column(db.Integer, primary_key=True)
    id_terapia = db.Column(db.Integer, db.ForeignKey('terapia.id', ondelete='CASCADE'), nullable=False)
    texto = db.Column(db.String(300), nullable=False)

    terapia = db.relationship('Terapia', backref=db.backref('laudos', lazy=True, cascade="all, delete"))

    def to_dict(self):
        return {
            'id': self.id,
            'id_terapia': self.id_terapia,
            'texto': self.texto
        }
    
    @staticmethod
    def validar_laudo(dados):
        erros = []

        id_terapia = dados.get('id_terapia')
        texto = dados.get('texto')

        if not id_terapia:
            erros.append('O campo id_terapia é obrigatório.')

        if not texto or len(texto.strip()) < 3:
            erros.append('A descrição deve ter pelo menos 3 caracteres.')

        return erros
    
    @staticmethod
    def listar_laudos():
        laudos = Laudo.query.all()
        return [laudo.to_dict() for laudo in laudos], 200
    
    @staticmethod
    def obter_laudo(id):
        laudo = Laudo.query.get(id)
        if not laudo:
            return {'erro': 'Laudo não encontrado'}, 404
        return laudo.to_dict(), 200
    
    @staticmethod
    def adicionar_laudo(dados):
        erros = Laudo.validar_laudo(dados)
        if erros:
            return {'erros': erros}, 400
        
        novo = Laudo(
            id_terapia=dados.get('id_terapia'),
            texto=dados.get('texto')
        )

        db.session.add(novo)
        db.session.commit()
        return {'mensagem': 'Laudo criado com sucesso', 'Laudo': novo.to_dict()}, 201
    
    @staticmethod
    def atualizar_laudo(dados):
        laudo = Laudo.query.get(dados.get('id'))
        if not laudo:
            return {'erro': 'Sala não encontrada'}, 404
        
        laudo.id_terapia = dados.get('id_terapia', laudo.id_terapia)
        laudo.texto = dados.get('texto', laudo.texto)

        erros = Laudo.validar_laudo(dados)
        if erros:
            return {'erros': erros}, 400
        
        db.session.commit()
        return {'mensagem': 'Laudo atualizado com sucesso', 'Laudo': laudo.to_dict()}, 200
    
    @staticmethod
    def deletar_laudo(id):
        laudo = Laudo.query.get(id)
        if not laudo:
            return {'erro': 'Laudo não encontrado'}, 404
        
        db.session.delete(laudo)
        db.session.commit()
        return {'mensagem': 'Laudo deletado com sucesso'}, 200