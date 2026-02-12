
from sqlalchemy import func
from . import db, login_manager
from datetime import datetime, timezone
from flask_login import UserMixin

@login_manager.user_loader
def load_usuario(id_usuario):
    usuario = Usuario.query.get(id_usuario)
    return usuario

class Usuario(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    fotos = db.relationship('Foto', backref='usuario', lazy=True)


    def __repr__(self):
        return f"Usuario('{self.username}', '{self.email}')"

class Foto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    imagem = db.Column(db.String(80), default='default.jpg', nullable=False)
    descricao = db.Column(db.String(80), nullable=True)
    data_criacao = db.Column(db.DateTime, nullable=False, default=func.now())
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)

    def __repr__(self):
        return f"Foto('{self.imagem}', '{self.descricao}', '{self.data_criacao}')"