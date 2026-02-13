from crypt import methods
from flask import Flask, render_template, url_for, redirect, flash
from flask_login import login_required, login_user, logout_user, current_user
from sqlalchemy.sql.functions import user
from wtforms import Form
from pinterest import app, db, bcrypt
from pinterest.models import Usuario, Foto
from pinterest.forms import FormCriarConta, FormLogin, FormFoto
import os
from werkzeug.utils import secure_filename

@app.route('/', methods=['GET', 'POST'])
@app.route('/home', methods=['GET', 'POST'])
def homepage():
    form = FormLogin()
    if form.validate_on_submit():
        usuario = Usuario.query.filter_by(email=form.email.data).first()
        if usuario and bcrypt.check_password_hash(usuario.password, form.password.data):
            login_user(usuario, remember=form.remember_me.data)
            return redirect(url_for('perfil', id_usuario=usuario.id))
        flash('Email ou senha incorretos.', 'alert-danger')
    return render_template('homepage.html', form=form)

@app.route('/criarconta', methods=['GET', 'POST'])
def criarconta():
    form =  FormCriarConta()
    if form.validate_on_submit():
        usuario = Usuario()
        usuario.email = form.email.data
        usuario.username = form.username.data
        usuario.password = bcrypt.generate_password_hash(form.password.data)

        db.session.add(usuario)
        db.session.commit()

        ## aqui é onde você processaria os dados do formulário, como criar um novo usuário
        ## e salvar no banco de dados. Por enquanto, vamos apenas imprimir os dados no console.
        print(f"Username: {form.username.data}")
        print(f"Email: {form.email.data}")
        print(f"Password: {form.password.data}")
        ## força o login
        login_user(usuario, remember=True)
        # Redirecionar para a página de login ou perfil após criar a conta
        return redirect( url_for('perfil', id_usuario=usuario.id))  # Redireciona para a homepage ou outra página após criar a conta
    return render_template('criarconta.html', form=form)


@login_required
@app.route('/perfil/<id_usuario>', methods=['GET', 'POST'])
def perfil(id_usuario):
    try:
        id_int = int(id_usuario)
    except (TypeError, ValueError):
        return redirect(url_for('homepage'))
    if current_user.is_authenticated and current_user.id is not None and id_int == current_user.id:
        form_foto = FormFoto()
        if form_foto.validate_on_submit():
            arquivo = form_foto.foto.data
            nome_seguro = secure_filename(arquivo.filename)
            
            ## pegando o caminho do projeto:
            ## os.path.abspath(os.path.dirname(__file__)
            caminho_arquivo = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                app.config['UPLOADER_FOLDER'], nome_seguro) 
            arquivo.save(caminho_arquivo)
            foto = Foto(id_usuario=current_user.id, imagem=nome_seguro, descricao='descricao da foto')
            
            db.session.add(foto)
            db.session.commit()
        ## usuario acesso seu perfil
        return render_template('perfil.html', usuario=current_user, form=form_foto)
    else:
        user = Usuario.query.get(id_int)
        if user is None:
            return redirect(url_for('homepage'))
        return render_template('perfil.html', usuario=user, form=None)

@app.route('/logout')
@login_required
def logout():
    ## aqui ele pega o current_user e "desloga"
    logout_user()
    return redirect(url_for('homepage'))

@app.route('/feed')
@login_required
def feed():
    fotos = Foto.query.order_by(Foto.data_criacao.desc()).all()
    return render_template('feed.html', fotos=fotos)