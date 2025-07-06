import os
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# === 1. Configurações iniciais ===

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)

db_path = os.path.join(basedir, 'data', 'banco.db')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# === 2. Modelo de Cliente ===

class Cliente(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True)
    telefone = db.Column(db.String(20))
    como_conheceu = db.Column(db.String(100))

    def __repr__(self):
        return f'<Cliente {self.nome}>'

# === 3. Contexto para mostrar a data atual nos templates ===

@app.context_processor
def inject_now():
    return {'now': datetime.utcnow}

# === 4. Rotas ===

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/produtos')
def cadastro_produtos():
    return render_template('coming_soon.html', módulo='Cadastro de Produtos')

# 👉 GET: mostrar formulário + clientes
@app.route('/clientes')
def cadastro_clientes():
    clientes = Cliente.query.all()
    return render_template('cadastro_clientes.html', clientes=clientes)

# 👉 POST: salvar novo cliente
@app.route('/clientes', methods=['POST'])
def cadastro_clientes_post():
    nome = request.form['nome']
    email = request.form['email']
    telefone = request.form['telefone']
    como = request.form['como_conheceu']

    novo = Cliente(nome=nome, email=email, telefone=telefone, como_conheceu=como)
    db.session.add(novo)
    db.session.commit()

    return redirect(url_for('cadastro_clientes'))

@app.route('/os')
def os_listar():
    return render_template('coming_soon.html', módulo='Listagem de OS')

# === 5. Criar o banco e rodar o app ===

if __name__ == '__main__':
    os.makedirs(os.path.join(basedir, 'data'), exist_ok=True)
    with app.app_context():
        db.create_all()
    app.run(debug=True)
