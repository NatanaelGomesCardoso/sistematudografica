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


# --- 2. MODELOS DO BANCO DE DADOS (COM TODOS OS CAMPOS) ---
class Cliente(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tipo = db.Column(db.String(10), nullable=False)

    # Campos Pessoa Física
    nome = db.Column(db.String(100))
    cpf = db.Column(db.String(20), unique=True)
    email = db.Column(db.String(120))
    endereco_entrega_pf = db.Column(db.String(255)) # Novo

    # Campos Pessoa Jurídica
    razao_social = db.Column(db.String(100))
    cnpj = db.Column(db.String(20), unique=True)
    email_cnpj = db.Column(db.String(120))
    endereco_empresa = db.Column(db.String(255)) # Novo
    endereco_entrega_pj = db.Column(db.String(255)) # Novo

    # Campo Comum
    telefone = db.Column(db.String(30), nullable=False)

    def __repr__(self):
        return f'<Cliente {self.nome or self.razao_social}>'


# --- 3. ROTAS DO SISTEMA ---
@app.context_processor
def inject_now():
    return {'now': datetime.utcnow}

@app.route('/')
def home():
    return render_template('home.html')

# NOVA ROTA: Listar e Pesquisar Clientes
@app.route('/clientes')
def pesquisar_clientes():
    query = request.args.get('q', '') # Pega o termo de busca da URL, se houver
    if query:
        # Busca por nome, razao_social, cpf ou cnpj
        search_term = f"%{query}%"
        clientes = Cliente.query.filter(or_(
            Cliente.nome.ilike(search_term),
            Cliente.razao_social.ilike(search_term),
            Cliente.cpf.ilike(search_term),
            Cliente.cnpj.ilike(search_term)
        )).all()
    else:
        clientes = Cliente.query.all() # Se não houver busca, lista todos
        
    return render_template('pesquisar_clientes.html', clientes=clientes, query=query)

# Rota para a página de cadastro (GET)
@app.route('/clientes/novo')
def cadastro_clientes():
    return render_template('cadastro_clientes.html')

# Rota que recebe os dados do formulário (POST)
@app.route('/clientes/novo', methods=['POST'])
def cadastro_clientes_post():
    tipo = request.form.get('tipo')

    if tipo == 'cpf':
        if request.form.get('cpf'):
            if Cliente.query.filter_by(cpf=request.form.get('cpf')).first():
                return "Erro: CPF já cadastrado!", 400
        
        novo_cliente = Cliente(
            tipo='cpf',
            nome=request.form.get('nome'),
            telefone=request.form.get('telefone'),
            cpf=request.form.get('cpf'),
            email=request.form.get('email'),
            endereco_entrega_pf=request.form.get('endereco_entrega_pf')
        )
    elif tipo == 'cnpj':
        if request.form.get('cnpj'):
            if Cliente.query.filter_by(cnpj=request.form.get('cnpj')).first():
                return "Erro: CNPJ já cadastrado!", 400
                
        novo_cliente = Cliente(
            tipo='cnpj',
            razao_social=request.form.get('razao_social'),
            telefone=request.form.get('telefone'),
            cnpj=request.form.get('cnpj'),
            email_cnpj=request.form.get('email_cnpj'),
            endereco_empresa=request.form.get('endereco_empresa'),
            endereco_entrega_pj=request.form.get('endereco_entrega_pj')
        )
    else:
        return "Erro: tipo de cadastro inválido", 400

    db.session.add(novo_cliente)
    db.session.commit()
    # Redireciona para a lista de clientes com mensagem de sucesso (faremos no futuro)
    return redirect(url_for('pesquisar_clientes'))

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