from flask_sqlalchemy import SQLAlchemy # type: ignore
from datetime import date
from werkzeug.security import generate_password_hash, check_password_hash # type: ignore
from .extensions import login_manager, db
from flask_login import UserMixin
from datetime import datetime

@login_manager.user_loader
def load_user(id):
    return Usuario.query.get(int(id))

filme_genero = db.Table('filme_genero',
    db.Column('genero_id', db.Integer, db.ForeignKey('genero.id'), primary_key=True),
    db.Column('filme_id', db.Integer, db.ForeignKey('filme.id'), primary_key=True)
)

usuario_filme_fav = db.Table('usuario_filme_fav',
    db.Column('usuario_id', db.Integer, db.ForeignKey('usuario.id'), primary_key=True),
    db.Column('filme_id', db.Integer, db.ForeignKey('filme.id'), primary_key=True)
)

usuario_ator_fav = db.Table('usuario_ator_fav',
    db.Column('usuario_id', db.Integer, db.ForeignKey('usuario.id'), primary_key=True),
    db.Column('ator_id', db.Integer, db.ForeignKey('ator.id'), primary_key=True)
)

class Filme(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100), nullable=False)
    tipo = db.Column(db.String(10), nullable=False)
    descricao = db.Column(db.Text, nullable=False)
    temporada = db.Column(db.Integer, nullable=True)
    trailer = db.Column(db.String(50), nullable=True)
    data_lancamento = db.Column(db.Date, nullable=True)

    avaliacoes = db.relationship('Avaliacao', back_populates='filme', cascade='all, delete-orphan')
    episodios = db.relationship('Episodio', backref='filme', lazy=True)
    atuacoes = db.relationship("Atuacao", back_populates='filme', cascade='all, delete-orphan')
    generos = db.relationship('Genero', secondary=filme_genero, back_populates='filmes')
    status_filme = db.relationship('Status', back_populates='filme', cascade='all, delete-orphan')

    @property
    def ano(self):
        if self.data_lancamento:
            return self.data_lancamento.year
        return None

    @property
    def media(self):
        if self.episodios:
            media = sum(nota.avaliacao for nota in self.episodios) / len(self.episodios)
            media = round(media, 2)
            return media
        else:
            media = None
        return media

class Episodio(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100), nullable=False)
    numero = db.Column(db.String(10), nullable=False)
    filme_id = db.Column(db.Integer, db.ForeignKey('filme.id', name='fk_episodio_filme_id'), nullable=False)

    def __repr__(self):
        return f"<Episodio {self.numero} - {self.titulo}>"
    
class Ator(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    data_nascimento = db.Column(db.Date, nullable=True)

    atuacoes = db.relationship("Atuacao", back_populates='ator', cascade='all, delete-orphan')

    @property
    def idade(self):
        hoje = date.today()
        return hoje.year - self.data_nascimento.year - ((hoje.month, hoje.day) < (self.data_nascimento.month, self.data_nascimento.day))

class Atuacao(db.Model):
    __tablename__ = 'atuacao'

    ator_id = db.Column(db.Integer, db.ForeignKey('ator.id'), primary_key=True)
    filme_id = db.Column(db.Integer, db.ForeignKey('filme.id'), primary_key=True)
    personagem = db.Column(db.String(100), nullable=True)

    ator = db.relationship('Ator', back_populates='atuacoes')
    filme = db.relationship('Filme', back_populates='atuacoes')

class Genero(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    nome = db.Column(db.String(50), nullable=False)

    filmes = db.relationship('Filme', secondary=filme_genero, back_populates='generos')

class Usuario(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key = True)
    nome = db.Column(db.String(100), nullable=False)
    usuario = db.Column(db.String(50), name='fk_avaliacao_usuario_id', unique=True, nullable=False)
    senha_hash = db.Column(db.String(100), nullable=False)
    foto_url = db.Column(db.Text, nullable=True)
    descricao = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow) 

    avaliacoes = db.relationship('Avaliacao', back_populates='usuario', cascade='all, delete-orphan')

    filmes_fav = db.relationship('Filme',
        secondary=usuario_filme_fav,
        backref=db.backref('usuarios_favoritaram', lazy='dynamic'),
        lazy='dynamic')
    
    atores_fav = db.relationship('Ator',
        secondary=usuario_ator_fav,
        backref=db.backref('usuarios_favoritaram', lazy='dynamic'),
        lazy='dynamic')

    status_filme = db.relationship('Status', back_populates='usuario', cascade='all, delete-orphan')

    def set_senha(self, senha):
        self.senha_hash = generate_password_hash(senha)

    def verificar_senha(self, senha):
        return check_password_hash(self.senha_hash, senha)


class Status(db.Model):
    __tablename__ = 'status'

    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), primary_key=True)
    filme_id = db.Column(db.Integer, db.ForeignKey('filme.id'), primary_key=True)
    status= db.Column(db.String(20), nullable=False)

    usuario = db.relationship('Usuario', back_populates='status_filme')
    filme = db.relationship('Filme', back_populates='status_filme')

class Avaliacao(db.Model):
    __tablename__ = 'avaliacao'
    
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), primary_key=True)
    filme_id = db.Column(db.Integer, db.ForeignKey('filme.id'), primary_key=True)
    nota = db.Column(db.Float, nullable=False)
    comentario = db.Column(db.Text, nullable = True)

    usuario = db.relationship('Usuario', back_populates='avaliacoes')
    filme = db.relationship('Filme', back_populates='avaliacoes')