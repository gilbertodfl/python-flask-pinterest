
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

# Configuração do banco
database_url = os.getenv('DATABASE_URL')

app.logger.warning("=== INICIANDO CONFIGURACAO DO BANCO ===")
app.logger.warning(f"DATABASE_URL encontrada: {bool(database_url)}")

if database_url:
    if database_url.startswith('postgres://'):
        database_url = database_url.replace(
            'postgres://', 'postgresql://', 1
        )

    if database_url.startswith('postgresql://'):
        database_url = database_url.replace(
            'postgresql://',
            'postgresql+psycopg://',
            1
        )

    app.config['SQLALCHEMY_DATABASE_URI'] = database_url

else:
    if os.getenv('RENDER'):
        raise RuntimeError(
            "DATABASE_URL nao configurada no ambiente Render!"
        )

    app.logger.warning("Utilizando SQLite local")
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

# Inicialização das extensões
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'alert-info'

# Registrar modelos
from . import models

# Diagnóstico e criação das tabelas
with app.app_context():
    try:
        engine = db.engine
        url = engine.url

        app.logger.warning(
            f"Banco utilizado: {url.get_backend_name()}"
        )
        app.logger.warning(f"Host: {url.host}")
        app.logger.warning(f"Database: {url.database}")

        with engine.connect() as connection:
            connection.execute(sqlalchemy.text("SELECT 1"))

        app.logger.warning("Conexao com banco estabelecida!")

        db.create_all()

        inspector = sqlalchemy.inspect(engine)
        tabelas = inspector.get_table_names()

        app.logger.warning(f"Tabelas encontradas: {tabelas}")
        app.logger.warning("=== INICIALIZACAO CONCLUIDA ===")

    except Exception:
        app.logger.exception("ERRO NA INICIALIZACAO DO BANCO")
        raise

# Importar rotas por último
from . import routes
