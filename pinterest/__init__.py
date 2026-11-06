## configuração inicial do projeto Flask

from flask import Flask

from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
import sqlalchemy

import os 
## https://flask-wtf.readthedocs.io/en/stable/

## https://flask.palletsprojects.com/en/stable/

app = Flask(__name__)

app.config['SECRET_KEY'] ='84741a09e5e38f33ac7410686aa03a5d'
app.config['UPLOADER_FOLDER'] = 'static/fotos_posts'
if os.getenv('DATABASE_URL'):
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

## create the SQLAlchemy db instance
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
## o login_view define qual função de rota vai ser chamada quando um usuário
## tentar acessar uma rota protegida sem estar logado.
## Observe que 'login' é o nome da função de rota definida em routes.py
login_manager.login_view = 'login'
login_manager.login_message_category = 'alert-info'

#criando o engine para o banco de dados
from . import models

## parece que na produção não está indo para postgres, então vamos criar as tabelas manualmente se não existirem
# engine = sqlalchemy.create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
# inspector = sqlalchemy.inspect(engine)
# if not inspector.has_table('usuario'):
#     with app.app_context():
#         db.create_all()
#         print("Tabelas criadas!")
# else:
#     print("Tabelas já existem!")
###########################################

# Importa os modelos para registrar as tabelas
from . import models

# Diagnóstico da inicialização do banco
with app.app_context():

    try:
        # Verifica qual banco está configurado
        engine = db.engine
        url = engine.url

        app.logger.info("=" * 50)
        app.logger.info("INICIALIZACAO DO BANCO DE DADOS")
        app.logger.info("=" * 50)

        app.logger.info(
            f"DATABASE_URL configurada: {bool(os.getenv('DATABASE_URL'))}"
        )

        app.logger.info(f"Banco utilizado: {url.get_backend_name()}")
        app.logger.info(f"Host: {url.host or 'Local'}")
        app.logger.info(f"Database: {url.database}")

        # Testa a conexão
        with engine.connect() as connection:
            connection.execute(sqlalchemy.text("SELECT 1"))

        app.logger.info("Conexao com banco estabelecida!")

        # Verifica as tabelas
        inspector = sqlalchemy.inspect(engine)
        tabelas = inspector.get_table_names(schema='public') if url.get_backend_name() == 'postgresql' else inspector.get_table_names()

        app.logger.info(f"Tabelas encontradas: {tabelas}")

        # Cria as tabelas ausentes
        db.create_all()

        inspector = sqlalchemy.inspect(engine)
        tabelas = inspector.get_table_names(schema='public') if url.get_backend_name() == 'postgresql' else inspector.get_table_names()

        app.logger.info(f"Tabelas apos create_all: {tabelas}")

        app.logger.info("INICIALIZACAO CONCLUIDA!")

    except Exception:
        app.logger.exception("ERRO NA INICIALIZACAO DO BANCO DE DADOS")
        raise
## as rotas e modelos foram movidos para o pacote pinterest
## precisam ser chamadas logo após a criação do app Flask
## portanto, não mude de lugar essa importação.

from . import routes
    