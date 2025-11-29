from flask import Flask, render_template, request, jsonify
from db import init_db, listar_historico
from services import produtos_service

app = Flask(__name__)

# Inicializa o banco ao rodar
init_db()

@app.route('/')
def index():
    return render_template('index.html')

# --- ROTAS DE PRODUTOS ---

@app.route('/api/produtos', methods=['GET'])
def get_produtos():
    categoria = request.args.get('categoria')
    produtos = produtos_service.listar_produtos(categoria)
    return jsonify(produtos)

@app.route('/api/adicionar', methods=['POST'])
def add_produto():
    data = request.json
    resultado = produtos_service.criar_produto(data)
    
    status_code = 201 if resultado['success'] else 400
    return jsonify(resultado), status_code

@app.route('/api/atualizar/<int:produto_id>', methods=['PUT'])
def update_produto(produto_id):
    data = request.json
    resultado = produtos_service.editar_produto(produto_id, data)
    
    status_code = 200 if resultado['success'] else 500
    return jsonify(resultado), status_code

@app.route('/api/deletar/<int:id>', methods=['DELETE'])
def delete_produto(id):
    resultado = produtos_service.remover_produto(id)
    
    status_code = 200 if resultado['success'] else 500
    return jsonify(resultado), status_code

# --- ROTA DE HISTÓRICO ---

@app.route('/api/historico', methods=['GET'])
def get_historico():
    logs = listar_historico()
    return jsonify(logs)

if __name__ == '__main__':
    app.run(debug=True)