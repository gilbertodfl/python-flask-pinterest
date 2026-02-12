from pinterest import db, app

## preciso importar os modelos para criar as tabelas no banco de dados
from pinterest.models import Usuario, Foto

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

## rode no comando de linha: python create_db.py

with app.app_context():
    db.create_all()
    print('abrindo o banco de dados...')

print("Database created successfully: veja em instance/database.db")