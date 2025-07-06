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
    tipo = db.Column(db.String(10))  # 'cpf' ou 'cnpj'

    # Pessoa Física
    nome = db.Column(db.String(100))
    cpf = db.Column(db.String(20))
    email = db.Column(db.String(120))

    # Pessoa Jurídica
    razao_social = db.Column(db.String(100))
    nome_fantasia = db.Column(db.String(100))
    cnpj = db.Column(db.String(20))
    responsavel = db.Column(db.String(100))
    telefone_empresa = db.Column(db.String(30))
    email_cnpj = db.Column(db.String(120))
    endereco_empresa = db.Column(db.String(255))
    endereco_entrega = db.Column(db.String(255))

    # Comum
    telefone = db.Column(db.String(30))
    como_conheceu = db.Column(db.String(100))
    como_conheceu_outros = db.Column(db.String(100))

    def __repr__(self):
        return f'<Cliente {self.nome or self.razao_social}>'


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


@app.route('/clientes', methods=['POST'])
def cadastro_clientes_post():
    tipo = request.form['tipo']

    if tipo == 'cpf':
        cliente = Cliente(
            tipo='cpf',
            nome=request.form['nome'],
            cpf=request.form['cpf'],
            email=request.form['email'],
            telefone=request.form['telefone'],
            como_conheceu=request.form['como_conheceu'],
            como_conheceu_outros=request.form.get('como_conheceu_outros', '')
        )
    else:
        cliente = Cliente(
            tipo='cnpj',
            razao_social=request.form['razao_social'],
            nome_fantasia=request.form['nome_fantasia'],
            cnpj=request.form['cnpj'],
            responsavel=request.form['responsavel'],
            telefone_empresa=request.form['telefone_empresa'],
            email_cnpj=request.form['email_cnpj'],
            endereco_empresa=request.form['endereco_empresa'],
            endereco_entrega=request.form['endereco_entrega'],
            telefone=request.form['telefone'],
            como_conheceu=request.form['como_conheceu'],
            como_conheceu_outros=request.form.get('como_conheceu_outros', '')
        )

    db.session.add(cliente)
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
