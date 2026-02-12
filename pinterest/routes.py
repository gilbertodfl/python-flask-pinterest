from flask import Flask, render_template, url_for, redirect
from flask_login import login_required, login_user, logout_user, current_user
from sqlalchemy.sql.functions import user
from wtforms import Form
from pinterest import app, db, bcrypt
from pinterest.models import Usuario, Foto
from pinterest.forms import FormCriarConta, FormLogin


@app.route('/')
@app.route('/home', methods=['GET', 'POST'])
def homepage():
    form = FormLogin()
    if form.validate_on_submit():
        usuario = Usuario.query.filter_by(email=form.email.data).first()
        if usuario and  bcrypt.check_password_hash(usuario.password, form.password.data):
                login_user(usuario, remember=form.remember_me.data)
                return redirect(url_for('perfil', usuario=usuario.username))
    return render_template('homepage.html', form=form)

@app.route('/criarconta', methods=['GET', 'POST'])
def criarconta():
    form =  FormCriarConta()
    if form.validate_on_submit():
        usuario = Usuario()
        usuario.email = form.email.data
        usuario.username = form.username.data
        usuario.password = bcrypt.generate_password_hash(form.username.data)

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
        return redirect( url_for('perfil', usuario=usuario.username))  # Redireciona para a homepage ou outra página após criar a conta
    return render_template('criarconta.html', form=form)


@login_required
@app.route('/perfil/<usuario>')
def perfil(usuario):
    return render_template('perfil.html', usuario=usuario)

@app.route('/logout')
@login_required
def logout():
    ## aqui ele pega o current_user e "desloga"
    logout_user()
    return redirect(url_for('homepage'))
