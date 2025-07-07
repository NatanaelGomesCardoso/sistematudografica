import os
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy import or_

# --- 1. CONFIGURAÇÃO INICIAL ---
basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
db_path = os.path.join(basedir, 'data', 'banco.db')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# --- 2. MODELOS DO BANCO DE DADOS (COM CAMPOS ATUALIZADOS) ---
class Cliente(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tipo = db.Column(db.String(10), nullable=False)

    # Campos Pessoa Física
    nome = db.Column(db.String(100))
    cpf = db.Column(db.String(20), unique=True)
    email = db.Column(db.String(120))
    endereco_entrega_pf = db.Column(db.String(255))

    # Campos Pessoa Jurídica
    razao_social = db.Column(db.String(100))
    cnpj = db.Column(db.String(20), unique=True)
    email_cnpj = db.Column(db.String(120))
    endereco_empresa = db.Column(db.String(255))
    endereco_entrega_pj = db.Column(db.String(255))

    # Campos Comuns
    telefone = db.Column(db.String(30), nullable=False)
    como_conheceu = db.Column(db.String(100)) # Campo adicionado
    como_conheceu_outros = db.Column(db.String(100)) # Campo adicionado

    def __repr__(self):
        return f'<Cliente {self.nome or self.razao_social}>'


# --- 3. ROTAS DO SISTEMA ---
@app.context_processor
def inject_now():
    return {'now': datetime.utcnow}

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/clientes')
def pesquisar_clientes():
    query = request.args.get('q', '')
    if query:
        search_term = f"%{query}%"
        clientes = Cliente.query.filter(or_(
            Cliente.nome.ilike(search_term),
            Cliente.razao_social.ilike(search_term),
            Cliente.cpf.ilike(search_term),
            Cliente.cnpj.ilike(search_term)
        )).all()
    else:
        clientes = Cliente.query.all()
        
    return render_template('pesquisar_clientes.html', clientes=clientes, query=query)

@app.route('/clientes/novo')
def cadastro_clientes():
    return render_template('cadastro_clientes.html')

@app.route('/clientes/novo', methods=['POST'])
def cadastro_clientes_post():
    tipo = request.form.get('tipo')

    # Pega os dados do formulário, tratando campos vazios como None
    # Isso corrige o erro de UNIQUE constraint para campos opcionais
    cpf = request.form.get('cpf') or None
    cnpj = request.form.get('cnpj') or None
    
    # Validação para não aceitar dois clientes com o mesmo CPF/CNPJ não-nulo
    if tipo == 'cpf' and cpf and Cliente.query.filter_by(cpf=cpf).first():
        flash('Erro: Já existe um cliente com este CPF.', 'error')
        return redirect(url_for('cadastro_clientes'))
    if tipo == 'cnpj' and cnpj and Cliente.query.filter_by(cnpj=cnpj).first():
        flash('Erro: Já existe um cliente com este CNPJ.', 'error')
        return redirect(url_for('cadastro_clientes'))

    if tipo == 'cpf':
        novo_cliente = Cliente(
            tipo='cpf',
            nome=request.form.get('nome'),
            telefone=request.form.get('telefone'),
            como_conheceu=request.form.get('como_conheceu'),
            como_conheceu_outros=request.form.get('como_conheceu_outros', ''),
            cpf=cpf,
            email=request.form.get('email'),
            endereco_entrega_pf=request.form.get('endereco_entrega_pf')
        )
    elif tipo == 'cnpj':
        novo_cliente = Cliente(
            tipo='cnpj',
            razao_social=request.form.get('razao_social'),
            telefone=request.form.get('telefone'),
            cnpj=cnpj,
            como_conheceu=request.form.get('como_conheceu'),
            como_conheceu_outros=request.form.get('como_conheceu_outros', ''),
            email_cnpj=request.form.get('email_cnpj'),
            endereco_empresa=request.form.get('endereco_empresa'),
            endereco_entrega_pj=request.form.get('endereco_entrega_pj')
        )
    else:
        flash("Erro: tipo de cadastro inválido", 'error')
        return redirect(url_for('cadastro_clientes'))

    db.session.add(novo_cliente)
    db.session.commit()
    
    flash('Cliente cadastrado com sucesso!', 'success')
    return redirect(url_for('cadastro_clientes'))

@app.route('/produtos')
def cadastro_produtos():
    return render_template('coming_soon.html')

@app.route('/os')
def os_listar():
    return render_template('coming_soon.html')

# --- 4. EXECUÇÃO ---
if __name__ == '__main__':
    with app.app_context():
        os.makedirs(os.path.join(basedir, 'data'), exist_ok=True)
        db.create_all()
    app.run(debug=True)