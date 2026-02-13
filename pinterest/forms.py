from flask import Flask
from flask_wtf import FlaskForm
from pinterest.models import Usuario
## para criar os campos useremos wtforms
from wtforms import FormField, StringField, PasswordField, BooleanField, SubmitField, FileField, TextAreaField

## as validações são feitas no wtforms.validators, como por exemplo 
# DataRequired para campos obrigatórios, Length para limitar o número de caracteres,
#  Email para validar endereços de email, 
# EqualTo para comparar campos (como senha e confirmação de senha), 
# e ValidationError para criar mensagens de erro personalizadas.
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError

## OBSERVAÇÃO: instale o flask-wtf para criar os formulários. 
## pip install flask-wtf
class FormLogin(FlaskForm):
    email = StringField('Email', validators=[DataRequired('Preencha o emmail'), Email('email inválido')])
    password = PasswordField('Password', validators=[DataRequired('campo obrigatório'), Length(min=6,max=20)])
    remember_me = BooleanField('Remember Me')    
    botao_confirmacao = SubmitField('Login')    

class FormCriarConta(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=20)])
    checkpassword = PasswordField('rewrite Password', validators=[DataRequired(), EqualTo('password', message='Passwords must match')])
    botao_confirmacao = SubmitField('Criar conta')

    ## verificação personalizada para garantir que o email não esteja cadastrado
    def validate_email(self, email):
        ## observe que tem  email.data porque vem do formulário.
        usuario = Usuario.query.filter_by(email=email.data).first()
        if usuario:
            raise ValidationError('Email já cadastrado. Utilize outro email.')

class FormFoto(FlaskForm):
    foto = FileField('Foto', validators=[DataRequired()])
    botao_confirmacao = SubmitField('Enviar foto')