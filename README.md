criando o ambiente

\# Criar ambiente virtual no linux

python3 -m venv .venv

\# Ativar o ambiente

source .venv/bin/activate

### instala flask

pip install flask

```plaintext
checando a instalação:
 pip freeze
blinker==1.9.0
click==8.3.1
Flask==3.1.2
itsdangerous==2.2.0
Jinja2==3.1.6
MarkupSafe==3.0.3
Werkzeug==3.1.5
```

cd '/home/gilberto/APRENDIZADO/python/python impressionador/flask-pinteres'

flask  --app main --debug run

### Criando o databasde sqlite

crie o arquivo create\_db.py:

```plaintext

from pinterest import database, app


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

with app.app_context():
    database.create_all()
    print('abrindo o banco de dados...')

print("Database created successfully: veja em instance/database.db")    
```

rode : `## rode no comando de linha:`

`python create_db.py`

### criando o login

pip install flask\_bcrypt flaslogin

### formulários:

 _pip install flask-wtf_