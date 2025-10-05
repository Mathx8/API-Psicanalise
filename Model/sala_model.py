from config import db
import re

class Sala(db.Model):
    __tablename__ = 'sala'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), nullable=False)
    descricao = db.Column(db.String(200), nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'descricao': self.descricao
        }
    
    @staticmethod
    def validar_sala(dados):
        erros = []

        nome = dados.get('nome')
        descricao = dados.get('descricao')

        if not nome or len(nome.strip()) < 1:
            erros.append('O nome deve ter pelo menos 3 caracteres.')

        if not descricao or len(descricao.strip()) < 3:
            erros.append('A descrição deve ter pelo menos 3 caracteres.')

        return erros
    
    @staticmethod
    def listar_salas():
        salas = Sala.query.all()
        return [sala.to_dict() for sala in salas], 200
    
    @staticmethod
    def obter_sala(id):
        sala = Sala.query.get(id)
        if not sala:
            return {'erro': 'Sala não encontrada'}, 404
        return sala.to_dict(), 200
    
    @staticmethod
    def adicionar_sala(dados):
        erros = Sala.validar_sala(dados)
        if erros:
            return {'erros': erros}, 400
        
        novo = Sala(
            nome=dados.get('nome'),
            descricao=dados.get('descricao')
        )

        db.session.add(novo)
        db.session.commit()
        return {'mensagem': 'Sala criada com sucesso', 'Sala': novo.to_dict()}, 201

    @staticmethod
    def atualizar_sala(dados):
        sala = Sala.query.get(dados.get('id'))
        if not sala:
            return {'erro': 'Sala não encontrada'}, 404
        
        sala.nome = dados.get('nome', sala.nome)
        sala.descricao = dados.get('descricao', sala.descricao)

        erros = Sala.validar_sala(dados)
        if erros:
            return {'erros': erros}, 400
        
        db.session.commit()
        return {'mensagem': 'Sala atualizada com sucesso', 'Sala': sala.to_dict()}, 200
    
    @staticmethod
    def deletar_sala(id):
        sala = Sala.query.get(id)
        if not sala:
            return {'erro': 'Sala não encontrada'}, 404
        
        db.session.delete(sala)
        db.session.commit()
        return {'mensagem': 'Sala deletada com sucesso'}, 200