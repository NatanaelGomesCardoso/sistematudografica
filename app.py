import os
import csv
import io
from flask import Flask, render_template, request, redirect, url_for, flash, Response
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_
from datetime import datetime
from werkzeug.utils import secure_filename

# --- 1. CONFIGURAÇÃO INICIAL ---
basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config['SECRET_KEY'] = 'uma-chave-secreta-muito-segura'
db_path = os.path.join(basedir, 'data', 'banco.db')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# --- 2. MODELOS DO BANCO DE DADOS ---
class Cliente(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tipo = db.Column(db.String(10), nullable=False)
    nome = db.Column(db.String(100))
    cpf = db.Column(db.String(20), unique=True)
    email = db.Column(db.String(120))
    endereco_pf = db.Column(db.String(255))
    razao_social = db.Column(db.String(100))
    responsavel = db.Column(db.String(100))
    cnpj = db.Column(db.String(20), unique=True)
    email_cnpj = db.Column(db.String(120))
    telefone_empresa = db.Column(db.String(30))
    endereco_empresa_pj = db.Column(db.String(255))
    endereco_entrega_pj = db.Column(db.String(255))
    telefone = db.Column(db.String(30), nullable=False)
    como_conheceu = db.Column(db.String(100), nullable=False)
    como_conheceu_outros = db.Column(db.String(100))

# --- 3. ROTAS DO SISTEMA ---
@app.context_processor
def inject_now():
    return {'now': datetime.utcnow}

@app.route('/')
def home():
    return render_template('home.html')

# --- ROTAS DE CLIENTES ---
@app.route('/clientes')
def pesquisar_clientes():
    # ... (código existente)
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
    # ... (código existente)
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
            email_cnpj=request.form.get('email_cnpj'),
            endereco_pf=request.form.get('endereco_pf'),
            endereco_empresa_pj=request.form.get('endereco_empresa_pj'),
            endereco_entrega_pj=request.form.get('endereco_entrega_pj')
        )
        db.session.add(novo_cliente)
        db.session.commit()
        flash('Cliente cadastrado com sucesso!', 'success')
        return redirect(url_for('pesquisar_clientes'))
    return render_template('cadastro_clientes.html')


@app.route('/clientes/editar/<int:id>', methods=['GET', 'POST'])
def editar_cliente(id):
    # ... (código existente)
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
        cliente.endereco_pf = request.form.get('endereco_pf')
        cliente.endereco_empresa_pj = request.form.get('endereco_empresa_pj')
        cliente.endereco_entrega_pj = request.form.get('endereco_entrega_pj')
        
        db.session.commit()
        flash('Cliente atualizado com sucesso!', 'success')
        return redirect(url_for('pesquisar_clientes'))

    return render_template('editar_cliente.html', cliente=cliente)


@app.route('/clientes/excluir/<int:id>', methods=['POST'])
def excluir_cliente(id):
    # ... (código existente)
    cliente = db.get_or_404(Cliente, id)
    db.session.delete(cliente)
    db.session.commit()
    flash('Cliente excluído com sucesso!', 'success')
    return redirect(url_for('pesquisar_clientes'))

# --- NOVAS ROTAS DE BACKUP ---
@app.route('/backup')
def backup_page():
    return render_template('backup.html')

@app.route('/backup/exportar')
def exportar_backup():
    clientes = Cliente.query.all()
    
    # Cria um arquivo CSV em memória
    output = io.StringIO()
    writer = csv.writer(output)
    
    # Escreve o cabeçalho
    writer.writerow(Cliente.__table__.columns.keys())
    
    # Escreve os dados dos clientes
    for cliente in clientes:
        writer.writerow([getattr(cliente, c) for c in Cliente.__table__.columns.keys()])
    
    output.seek(0)
    
    return Response(
        output,
        mimetype="text/csv",
        headers={"Content-Disposition":"attachment;filename=backup_clientes.csv"}
    )

@app.route('/backup/importar', methods=['POST'])
def importar_backup():
    if 'backup_file' not in request.files:
        flash('Nenhum arquivo selecionado.', 'error')
        return redirect(url_for('backup_page'))
    
    file = request.files['backup_file']
    
    if file.filename == '':
        flash('Nenhum arquivo selecionado.', 'error')
        return redirect(url_for('backup_page'))

    if file and file.filename.endswith('.csv'):
        try:
            stream = io.StringIO(file.stream.read().decode("UTF-8"), newline=None)
            reader = csv.DictReader(stream)
            
            novos_clientes = 0
            clientes_ignorados = 0

            for row in reader:
                cpf = row.get('cpf') or None
                cnpj = row.get('cnpj') or None
                
                # Verifica se o cliente já existe
                existe = False
                if cpf and Cliente.query.filter_by(cpf=cpf).first():
                    existe = True
                if cnpj and Cliente.query.filter_by(cnpj=cnpj).first():
                    existe = True

                if existe:
                    clientes_ignorados += 1
                    continue

                # Cria o novo cliente
                cliente = Cliente(**row)
                db.session.add(cliente)
                novos_clientes += 1
            
            db.session.commit()
            flash(f'{novos_clientes} clientes importados com sucesso. {clientes_ignorados} clientes foram ignorados por já existirem.', 'success')

        except Exception as e:
            db.session.rollback()
            flash(f'Ocorreu um erro ao importar o arquivo: {e}', 'error')

        return redirect(url_for('backup_page'))

    flash('Arquivo inválido. Por favor, envie um arquivo .csv', 'error')
    return redirect(url_for('backup_page'))


# --- ROTAS FUTURAS (PLACEHOLDERS) ---
@app.route('/produtos/novo')
def cadastro_produto():
    return render_template('coming_soon.html', modulo='Cadastro de Produto')
@app.route('/produtos/consultar')
def consultar_produto():
    return render_template('coming_soon.html', modulo='Consulta de Produto')
@app.route('/vendas/orcamento/novo')
def novo_orcamento():
    return render_template('coming_soon.html', modulo='Novo Orçamento')
@app.route('/vendas/os/nova')
def nova_os():
    return render_template('coming_soon.html', modulo='Nova Ordem de Serviço')
@app.route('/vendas/orcamento/consultar')
def consultar_orcamento():
    return render_template('coming_soon.html', modulo='Consulta de Orçamento')
@app.route('/vendas/os/consultar')
def consultar_os():
    return render_template('coming_soon.html', modulo='Consulta de O.S.')


# --- EXECUÇÃO ---
if __name__ == '__main__':
    with app.app_context():
        os.makedirs(os.path.join(basedir, 'data'), exist_ok=True)
        db.create_all()
    app.run(debug=True)