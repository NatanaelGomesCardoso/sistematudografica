import os
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_

# =============================================================================
# 1. CONFIGURAÇÃO INICIAL DA APLICAÇÃO E DO BANCO DE DADOS
# =============================================================================
basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config['SECRET_KEY'] = 'uma-chave-secreta-muito-segura'
db_path = os.path.join(basedir, 'data', 'banco.db')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# =============================================================================
# 2. MODELOS DO BANCO DE DADOS
# =============================================================================
class Fornecedor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False, unique=True)
    contato = db.Column(db.String(100))
    telefone = db.Column(db.String(30))
    email = db.Column(db.String(120))

# =============================================================================
# 3. ROTAS DO SISTEMA
# =============================================================================

@app.route('/')
def home():
    return render_template('home.html')

# --- ROTAS DE FORNECEDORES ---
@app.route('/fornecedores')
def listar_fornecedores():
    query = request.args.get('q', '')
    if query:
        search_term = f"%{query}%"
        fornecedores = Fornecedor.query.filter(Fornecedor.nome.ilike(search_term)).order_by(Fornecedor.nome).all()
    else:
        fornecedores = Fornecedor.query.order_by(Fornecedor.nome).all()
    return render_template('fornecedores_listar.html', fornecedores=fornecedores, query=query)

@app.route('/fornecedores/novo', methods=['GET', 'POST'])
def cadastrar_fornecedor():
    if request.method == 'POST':
        nome = request.form.get('nome')
        if Fornecedor.query.filter(Fornecedor.nome.ilike(nome)).first():
            flash('Já existe um fornecedor com este nome.', 'error')
        else:
            novo_fornecedor = Fornecedor(
                nome=nome,
                contato=request.form.get('contato'),
                telefone=request.form.get('telefone'),
                email=request.form.get('email')
            )
            db.session.add(novo_fornecedor)
            db.session.commit()
            flash('Fornecedor cadastrado com sucesso!', 'success')
            return redirect(url_for('listar_fornecedores'))
    return render_template('fornecedores_cadastrar.html')

@app.route('/fornecedores/editar/<int:id>', methods=['GET', 'POST'])
def editar_fornecedor(id):
    fornecedor = db.get_or_404(Fornecedor, id)
    if request.method == 'POST':
        nome = request.form.get('nome')
        if Fornecedor.query.filter(Fornecedor.id != id, Fornecedor.nome.ilike(nome)).first():
            flash('Já existe outro fornecedor com este nome.', 'error')
        else:
            fornecedor.nome = nome
            fornecedor.contato = request.form.get('contato')
            fornecedor.telefone = request.form.get('telefone')
            fornecedor.email = request.form.get('email')
            db.session.commit()
            flash('Fornecedor atualizado com sucesso!', 'success')
            return redirect(url_for('listar_fornecedores'))
    return render_template('fornecedores_editar.html', fornecedor=fornecedor)

@app.route('/fornecedores/excluir/<int:id>', methods=['POST'])
def excluir_fornecedor(id):
    fornecedor = db.get_or_404(Fornecedor, id)
    db.session.delete(fornecedor)
    db.session.commit()
    flash('Fornecedor excluído com sucesso!', 'success')
    return redirect(url_for('listar_fornecedores'))

# --- ROTAS PLACEHOLDER PARA EVITAR ERROS DE BUILD ---

@app.route('/clientes')
def pesquisar_clientes(): return render_template('coming_soon.html', modulo='Pesquisar Clientes')

@app.route('/clientes/novo')
def cadastrar_cliente(): return render_template('coming_soon.html', modulo='Cadastrar Cliente')

@app.route('/produtos/cadastrar')
def cadastrar_produto(): return render_template('coming_soon.html', modulo='Cadastro de Produto')

@app.route('/produtos/consultar')
def consultar_produto(): return render_template('coming_soon.html', modulo='Consulta de Produtos')

@app.route('/vendas/orcamentos')
def listar_orcamentos(): return render_template('coming_soon.html', modulo='Orçamentos')

@app.route('/vendas/os')
def listar_os(): return render_template('coming_soon.html', modulo='Ordens de Serviço')

# ROTA ADICIONADA PARA CORRIGIR O ERRO ATUAL
@app.route('/producao')
def painel_producao(): return render_template('coming_soon.html', modulo='Painel de Produção')

@app.route('/backup')
def backup_page(): return render_template('coming_soon.html', modulo='Backup')


# --- EXECUÇÃO ---
if __name__ == '__main__':
    with app.app_context():
        os.makedirs(os.path.join(basedir, 'data'), exist_ok=True)
        db.create_all()
    app.run(debug=True, port=5001)