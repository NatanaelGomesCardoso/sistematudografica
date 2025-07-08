import os
import csv
import io
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_
from datetime import datetime
from werkzeug.utils import secure_filename

# =============================================================================
# 1. CONFIGURAÇÃO INICIAL DO APP E BANCO DE DADOS
# =============================================================================

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config['SECRET_KEY'] = 'uma-chave-secreta-muito-segura-para-as-flash-messages'
db_path = os.path.join(basedir, 'data', 'banco.db')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# =============================================================================
# 2. MODELOS DO BANCO DE DADOS (AS NOSSAS TABELAS)
# =============================================================================

# Tabela de Clientes
class Cliente(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tipo = db.Column(db.String(10), nullable=False)
    # Campos Pessoa Física
    nome = db.Column(db.String(100))
    cpf = db.Column(db.String(20), unique=True)
    email = db.Column(db.String(120))
    endereco_pf = db.Column(db.String(255))
    # Campos Pessoa Jurídica
    razao_social = db.Column(db.String(100))
    responsavel = db.Column(db.String(100))
    cnpj = db.Column(db.String(20), unique=True)
    email_cnpj = db.Column(db.String(120))
    telefone_empresa = db.Column(db.String(30))
    endereco_empresa_pj = db.Column(db.String(255))
    endereco_entrega_pj = db.Column(db.String(255))
    # Campos Comuns
    telefone = db.Column(db.String(30), nullable=False)
    como_conheceu = db.Column(db.String(100), nullable=False)
    como_conheceu_outros = db.Column(db.String(100))

# Tabela de Fornecedores (para produtos terceirizados)
class Fornecedor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False, unique=True)
    contato = db.Column(db.String(100))
    telefone = db.Column(db.String(30))
    email = db.Column(db.String(120))
    # Relacionamento com Matérias-Primas
    materias_primas = db.relationship('MateriaPrima', backref='fornecedor', lazy=True)

# Tabela de Matérias-Primas (base para a precificação)
class MateriaPrima(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False, unique=True)
    unidade_compra = db.Column(db.String(50)) # Ex: 'm²', 'unidade', 'barra'
    unidade_uso = db.Column(db.String(50)) # Ex: 'm linear', 'unidade', 'fração'
    valor_unidade_compra = db.Column(db.Float, nullable=False)
    # Chave estrangeira para o fornecedor
    fornecedor_id = db.Column(db.Integer, db.ForeignKey('fornecedor.id'), nullable=True)


# =============================================================================
# 3. ROTAS DO SISTEMA (OS LINKS DO NOSSO SITE)
# =============================================================================

# Rota Principal
@app.route('/')
def home():
    return render_template('home.html')

# --- ROTAS DO MÓDULO DE CLIENTES ---
@app.route('/clientes')
def pesquisar_clientes():
    clientes = Cliente.query.order_by(Cliente.id.desc()).all()
    return render_template('clientes_pesquisar.html', clientes=clientes)

@app.route('/clientes/novo', methods=['GET', 'POST'])
def cadastrar_cliente():
    if request.method == 'POST':
        # Aqui virá a lógica de salvar o cliente que já fizemos
        pass
    return render_template('clientes_cadastrar.html')

# --- ROTAS DO MÓDULO DE PRODUTOS ---
@app.route('/produtos/materias-primas')
def listar_materias_primas():
    # Futuramente, vamos listar as matérias-primas aqui
    return render_template('coming_soon.html', modulo='Consulta de Matérias-Primas')

@app.route('/produtos/novo')
def cadastrar_produto():
    return render_template('coming_soon.html', modulo='Cadastro de Produto')


# --- ROTAS DO MÓDULO DE VENDAS ---
@app.route('/vendas/orcamentos')
def listar_orcamentos():
    return render_template('coming_soon.html', modulo='Consulta de Orçamentos')

@app.route('/vendas/os')
def listar_os():
    return render_template('coming_soon.html', modulo='Consulta de Ordens de Serviço')


# --- ROTAS DOS OUTROS MÓDULOS (PLACEHOLDERS) ---
@app.route('/producao')
def painel_producao():
    return render_template('coming_soon.html', modulo='Painel de Produção (PCP)')

@app.route('/financeiro')
def painel_financeiro():
    return render_template('coming_soon.html', modulo='Painel Financeiro')

@app.route('/backup')
def backup_page():
    return render_template('coming_soon.html', modulo='Backup e Restauração')


# =============================================================================
# 4. EXECUÇÃO DO APP
# =============================================================================

if __name__ == '__main__':
    with app.app_context():
        # Garante que a pasta 'data' exista
        os.makedirs(os.path.join(basedir, 'data'), exist_ok=True)
        # Cria todas as tabelas definidas acima no banco de dados
        db.create_all()
    app.run(debug=True, port=5001)