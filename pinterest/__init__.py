
# Configuração inicial do projeto Flask

import os
import sqlalchemy

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)

app.config['SECRET_KEY'] = os.getenv(
    'SECRET_KEY',
    'chave-local-desenvolvimento'
)

app.config['UPLOADER_FOLDER'] = 'static/fotos_posts'

# Configuração do banco de dados
database_url = os.getenv('DATABASE_URL')

if database_url:
    app.config['SQLALCHEMY_DATABASE_URI'] = database_url
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

# Inicialização das extensões
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'alert-info'

# Importa os modelos para registrar as tabelas
from . import models

# Diagnóstico da inicialização do banco
with app.app_context():
    try:
        engine = db.engine
        url = engine.url

        app.logger.info("=" * 50)
        app.logger.info("INICIALIZACAO DO BANCO DE DADOS")
        app.logger.info("=" * 50)

        app.logger.info(
            f"DATABASE_URL configurada: {bool(database_url)}"
        )

        app.logger.info(f"Banco utilizado: {url.get_backend_name()}")
        app.logger.info(f"Host: {url.host or 'Local'}")
        app.logger.info(f"Database: {url.database}")

        # Testa a conexão
        with engine.connect() as connection:
            connection.execute(sqlalchemy.text("SELECT 1"))

        app.logger.info("Conexao com banco estabelecida!")

        # Verifica tabelas existentes
        inspector = sqlalchemy.inspect(engine)

        tabelas = inspector.get_table_names()

        app.logger.info(f"Tabelas encontradas: {tabelas}")

        # Cria tabelas que ainda não existem
        db.create_all()

        inspector = sqlalchemy.inspect(engine)
        tabelas = inspector.get_table_names()

        app.logger.info(f"Tabelas apos create_all: {tabelas}")

        app.logger.info("INICIALIZACAO CONCLUIDA!")
        app.logger.info("=" * 50)

    except Exception:
        app.logger.exception(
            "ERRO NA INICIALIZACAO DO BANCO DE DADOS"
        )
        raise

# Importa as rotas por último
from . import routes
