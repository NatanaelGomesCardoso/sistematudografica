import os
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_ # A importação foi movida para cá
from datetime import datetime

# --- 1. CONFIGURAÇÃO INICIAL ---
basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config['SECRET_KEY'] = 'uma-chave-secreta-muito-segura-para-as-flash-messages'
db_path = os.path.join(basedir, 'data', 'banco.db')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# --- 2. MODELOS DO BANCO DE DADOS ---
class Cliente(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tipo = db.Column(db.String(10), nullable=False)
    # Campos Pessoa Física
    nome = db.Column(db.String(100))
    cpf = db.Column(db.String(20), unique=True)
    email = db.Column(db.String(120))
    # Campos Pessoa Jurídica
    razao_social = db.Column(db.String(100))
    responsavel = db.Column(db.String(100))
    cnpj = db.Column(db.String(20), unique=True)
    email_cnpj = db.Column(db.String(120))
    telefone_empresa = db.Column(db.String(30))
    # Campos Comuns
    telefone = db.Column(db.String(30), nullable=False)
    como_conheceu = db.Column(db.String(100), nullable=False)
    como_conheceu_outros = db.Column(db.String(100))

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
            Cliente.nome.ilike(search_term), Cliente.razao_social.ilike(search_term),
            Cliente.cpf.ilike(search_term), Cliente.cnpj.ilike(search_term)
        )).order_by(Cliente.id.desc()).all()
    else:
        clientes = Cliente.query.order_by(Cliente.id.desc()).all()
    return render_template('pesquisar_clientes.html', clientes=clientes, query=query)

@app.route('/clientes/novo', methods=['GET', 'POST'])
def cadastro_clientes():
    if request.method == 'POST':
        tipo = request.form.get('tipo')
        cpf = request.form.get('cpf') or None
        cnpj = request.form.get('cnpj') or None
        
        if tipo == 'cpf' and cpf and Cliente.query.filter_by(cpf=cpf).first():
            flash('Erro: Já existe um cliente com este CPF.', 'error')
            return redirect(url_for('cadastro_clientes'))
        if tipo == 'cnpj' and cnpj and Cliente.query.filter_by(cnpj=cnpj).first():
            flash('Erro: Já existe um cliente com este CNPJ.', 'error')
            return redirect(url_for('cadastro_clientes'))

        novo_cliente = Cliente(
            tipo=tipo,
            nome=request.form.get('nome'),
            razao_social=request.form.get('razao_social'),
            responsavel=request.form.get('responsavel'),
            telefone=request.form.get('telefone'),
            telefone_empresa=request.form.get('telefone_empresa'),
            como_conheceu=request.form.get('como_conheceu'),
            como_conheceu_outros=request.form.get('como_conheceu_outros', ''),
            cpf=cpf,
            cnpj=cnpj,
            email=request.form.get('email'),
            email_cnpj=request.form.get('email_cnpj')
        )
        db.session.add(novo_cliente)
        db.session.commit()
        flash('Cliente cadastrado com sucesso!', 'success')
        return redirect(url_for('pesquisar_clientes'))
        
    return render_template('cadastro_clientes.html')

@app.route('/clientes/editar/<int:id>', methods=['GET', 'POST'])
def editar_cliente(id):
    cliente = db.get_or_404(Cliente, id)
    if request.method == 'POST':
        cpf = request.form.get('cpf') or None
        cnpj = request.form.get('cnpj') or None
        
        if cpf and Cliente.query.filter(Cliente.id != id, Cliente.cpf == cpf).first():
            flash('Erro: O CPF informado já pertence a outro cliente.', 'error')
            return render_template('editar_cliente.html', cliente=cliente)
        if cnpj and Cliente.query.filter(Cliente.id != id, Cliente.cnpj == cnpj).first():
            flash('Erro: O CNPJ informado já pertence a outro cliente.', 'error')
            return render_template('editar_cliente.html', cliente=cliente)

        cliente.tipo = request.form.get('tipo')
        cliente.nome = request.form.get('nome')
        cliente.razao_social = request.form.get('razao_social')
        cliente.responsavel = request.form.get('responsavel')
        cliente.telefone = request.form.get('telefone')
        cliente.telefone_empresa = request.form.get('telefone_empresa')
        cliente.como_conheceu = request.form.get('como_conheceu')
        cliente.como_conheceu_outros = request.form.get('como_conheceu_outros', '')
        cliente.cpf = cpf
        cliente.cnpj = cnpj
        cliente.email = request.form.get('email')
        cliente.email_cnpj = request.form.get('email_cnpj')
        
        db.session.commit()
        flash('Cliente atualizado com sucesso!', 'success')
        return redirect(url_for('pesquisar_clientes'))

    return render_template('editar_cliente.html', cliente=cliente)

@app.route('/clientes/excluir/<int:id>', methods=['POST'])
def excluir_cliente(id):
    cliente = db.get_or_404(Cliente, id)
    db.session.delete(cliente)
    db.session.commit()
    flash('Cliente excluído com sucesso!', 'success')
    return redirect(url_for('pesquisar_clientes'))

@app.route('/produtos')
def cadastro_produtos():
    return render_template('coming_soon.html', módulo='Cadastro de Produtos')

@app.route('/os')
def os_listar():
    return render_template('coming_soon.html', módulo='Listagem de OS')


# --- 4. EXECUÇÃO ---
if __name__ == '__main__':
    with app.app_context():
        os.makedirs(os.path.join(basedir, 'data'), exist_ok=True)
        db.create_all()
    app.run(debug=True)