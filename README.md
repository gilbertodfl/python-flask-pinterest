## PINTEREST - FAKE

OBJETIVO: Simular o site pinterest. 

Permite criar uma conta, depois da conta criada é possível anexar fotos

## Ferramentas:
Vamos usar python, flask, sqlite, bcrypt. 

### Criando o ambiente

```bash
# Criar ambiente virtual no linux
python3 -m venv .venv
# Ativar o ambiente
source .venv/bin/activate
```
### Instalar flask
```bash
> pip install flask
```
## Checando a instalação:
```plaintext
pip freeze

blinker==1.9.0
click==8.3.1
Flask==3.1.2
itsdangerous==2.2.0
Jinja2==3.1.6
MarkupSafe==3.0.3
Werkzeug==3.1.5
```
## Onde está na minha máquina e como rodar? 
cd '/home/gilberto/APRENDIZADO/HASHTAG/python impressionador/FLASK/flask-pinterest'

flask  --app main --debug run

### Criando o databasde sqlite

crie o arquivo create_db.py:

```plaintext
from pinterest import database, app

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

with app.app_context():
    database.create_all()
    print('abrindo o banco de dados...')

print("Database created successfully: veja em instance/database.db")    
```

## Criando o database sqlite
Rode no comando de linha:

`python3 create_db.py`

### criando o login
Precisamos de alguns módulos conforme abaixo
>pip install flask bcrypt flaslogin

### formulários:

> pip install flask-wtf

> pip install email-validator

### Sequencia de carregamento do site

    passo 01: no bash flask  --app main --debug run
    passo 02: o main importa app que está em  pinterest/__init__.py
    passo 03: O __init__ carrega   db = SQLAlchemy(app), bcrypt = Bcrypt(app),login_manager = oginManager(app)
    passo 04: o __init__ importa e  carrega routes.py subindo o site: from . import routes

## Estrutura de pastas e arquivos

```text
flask-pinterest/
├── main.py                 # Ponto de entrada: inicia o servidor Flask.
├── create_db.py            # Cria as tabelas do banco SQLite.
├── README.md               # Documentação do projeto.
└── pinterest/
    ├── __init__.py         # Cria e configura o app, banco, bcrypt e Flask-Login.
    ├── routes.py           # Define as URLs e o que acontece em cada requisição.
    ├── forms.py            # Define os formulários e suas regras de validação.
    ├── models.py           # Define os modelos/tabelas Usuario e Foto.
    ├── templates/          # Páginas HTML renderizadas pelo Flask.
    │   ├── homepage.html   # Página de login e template-base das outras páginas.
    │   ├── criarconta.html # Página de cadastro de usuário.
    │   ├── perfil.html     # Perfil e formulário de envio de fotos.
    │   ├── feed.html       # Feed com as fotos publicadas.
    │   └── navbar.html     # Barra de navegação reutilizada no perfil e no feed.
    ├── static/             # Arquivos públicos servidos diretamente pelo Flask.
    │   ├── css/style.css   # Estilos visuais da aplicação.
    │   ├── fotos_site/     # Imagens fixas da interface.
    │   └── fotos_posts/    # Fotos enviadas pelos usuários.
    └── Layout/             # Arquivos de layout/referência usados durante a montagem visual.
```

## Como as partes interagem

1. O navegador acessa uma URL, como `/`, `/criarconta` ou `/perfil/<id_usuario>`.
2. A rota correspondente em `routes.py` cria o formulário definido em `forms.py` e renderiza um arquivo de `templates/` com `render_template`.
3. Em `homepage.html`, os campos são exibidos por Jinja, por exemplo `form.email` e `form.password`. No envio do formulário, o navegador faz um `POST` para a mesma rota.
4. A rota chama `form.validate_on_submit()`. As regras declaradas em `forms.py` verificam os dados; se houver erro, ele fica disponível em `form.campo.errors` e o template exibe a mensagem e a classe `is-invalid` no campo.
5. O CSS em `static/css/style.css` formata as classes usadas pelos templates, incluindo `.input` e `.input.is-invalid`, que destaca em vermelho campos inválidos.
6. `perfil.html` e `feed.html` estendem `homepage.html` e incluem `navbar.html` com `{% include "navbar.html" %}`. Assim, a navegação para feed, perfil e logout fica centralizada em um único arquivo.
7. Imagens e CSS são referenciados com `url_for('static', filename='...')`; por isso o Flask encontra os arquivos dentro de `static/` e gera a URL correta.

    
## Como colocar na nuvem
pip freeze > requirementes

Crie o arquivo `ProcFile` com o contéudo:

    web: gunicorn main:app