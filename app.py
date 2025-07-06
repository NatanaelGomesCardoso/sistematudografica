from flask import Flask, render_template
from datetime import datetime

app = Flask(__name__)

@app.context_processor
def inject_now():
    return {'now': datetime.utcnow}

@app.route('/')
def home():
    return render_template('home.html')

# rotas vazias por enquanto
@app.route('/produtos')
def cadastro_produtos():
    return render_template('coming_soon.html', módulo='Cadastro de Produtos')

@app.route('/clientes')
def cadastro_clientes():
    return render_template('coming_soon.html', módulo='Cadastro de Clientes')

@app.route('/os')
def os_listar():
    return render_template('coming_soon.html', módulo='Listagem de OS')

if __name__ == '__main__':
    app.run(debug=True)
