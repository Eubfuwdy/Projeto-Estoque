from flask import Flask, render_template, request, jsonify
import sqlite3
from datetime import datetime

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('estoque.db')
    cursor = conn.cursor()
    # Cria a tabela garantindo as colunas NOVAS (categoria e tamanho)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS produtos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            codigo TEXT NOT NULL,
            nome TEXT NOT NULL,
            quantidade INTEGER NOT NULL,
            preco REAL NOT NULL,
            categoria TEXT,
            tamanho TEXT,
            UNIQUE(codigo, categoria)
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS historico (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            mensagem TEXT NOT NULL,
            data_hora TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

init_db()

@app.route('/')
def index():
    return render_template('index.html')

# Rota de Listagem (FILTRO POR CATEGORIA)
@app.route('/api/produtos')
def get_produtos():
    categoria = request.args.get('categoria')
    conn = sqlite3.connect('estoque.db')
    cursor = conn.cursor()
    
    if categoria:
        # Se veio filtro, busca só aquela categoria
        cursor.execute('SELECT * FROM produtos WHERE categoria = ?', (categoria,))
    else:
        # Se não veio filtro (ou deu erro), pega tudo
        cursor.execute('SELECT * FROM produtos')
        
    produtos = cursor.fetchall()
    conn.close()
    return jsonify(produtos)

# Rota de Adicionar
@app.route('/api/adicionar', methods=['POST'])
def add_produto():
    data = request.json
    try:
        conn = sqlite3.connect('estoque.db')
        cursor = conn.cursor()
        
        # Insere Categoria e Tamanho
        cursor.execute('''
            INSERT INTO produtos (codigo, nome, quantidade, preco, categoria, tamanho) 
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (data['codigo'], data['nome'], data['quantidade'], data['preco'], data['categoria'], data.get('tamanho')))
        
        conn.commit()
        conn.close()
        
        # Histórico com Tag da Categoria
        registrar_historico(f"[{data['categoria'].upper()}] Produto '{data['nome']}' criado.")
        
        return jsonify({'message': 'Produto adicionado!'}), 201
    except sqlite3.IntegrityError:
        return jsonify({'message': 'Erro: Código já existe!'}), 400
    except Exception as e:
        print(f"ERRO: {e}") # Mostra erro no terminal se houver
        return jsonify({'message': str(e)}), 500

# Rota de Atualizar
@app.route('/api/atualizar/<int:produto_id>', methods=['PUT'])
# No seu app.py

@app.route('/api/atualizar/<int:produto_id>', methods=['PUT']) 
def update_produto(produto_id):                                
    data = request.json
    try:
        conn = sqlite3.connect('estoque.db')
        cursor = conn.cursor()
        
        # Usa produto_id na busca
        cursor.execute('SELECT * FROM produtos WHERE id = ?', (produto_id,))
        produto_atual = cursor.fetchone()
        
        if not produto_atual:
            return jsonify({'message': 'Produto não encontrado!'}), 404

        antigo_nome = produto_atual[2]
        antigo_qtd = produto_atual[3]
        antigo_preco = produto_atual[4]
        
        # ... (sua lógica de pegar os dados: codigo, nome, etc) ...
        novo_codigo = data.get('codigo') or produto_atual[1]
        novo_nome = data.get('nome') or produto_atual[2]
        novo_quantidade = data.get('quantidade') or produto_atual[3]
        novo_preco = data.get('preco') or produto_atual[4]
        novo_categoria = data.get('categoria') or produto_atual[5]
        novo_tamanho = data.get('tamanho') or produto_atual[6]

        alteracoes = []
        
        if novo_nome != antigo_nome:
            alteracoes.append(f"Nome: '{antigo_nome}' -> '{novo_nome}'")
            
        # Nota: Convertemos para float/int para garantir comparação numérica correta
        if float(novo_quantidade) != float(antigo_qtd):
            alteracoes.append(f"Qtd: {antigo_qtd} -> {novo_quantidade}")
            
        if float(novo_preco) != float(antigo_preco):
            alteracoes.append(f"Preço: R${antigo_preco} -> R${novo_preco}")

        cursor.execute('''
            UPDATE produtos 
            SET codigo=?, nome=?, quantidade=?, preco=?, categoria=?, tamanho=? 
            WHERE id=?
        ''', (novo_codigo, novo_nome, novo_quantidade, novo_preco, novo_categoria, novo_tamanho, produto_id))
        
        conn.commit()
        conn.close()

        if alteracoes:
            msg_detalhada = f"Produto '{novo_nome}' editado. Mudanças: " + " | ".join(alteracoes)
            registrar_historico(msg_detalhada)
        else:
            registrar_historico(f"Produto '{novo_nome}' salvo (sem alterações visíveis).")
        
        registrar_historico(f"Produto '{novo_nome}' editado.")
        return jsonify({'message': 'Atualizado com sucesso!'})
    except Exception as e:
        return jsonify({'message': str(e)}), 500

# Rota de Deletar
@app.route('/api/deletar/<int:id>', methods=['DELETE'])
def delete_produto(id):
    try:
        conn = sqlite3.connect('estoque.db')
        cursor = conn.cursor()
        cursor.execute('SELECT nome FROM produtos WHERE id = ?', (id,))
        produto = cursor.fetchone()
        nome_produto = produto[0] if produto else "Desconhecido"

        cursor.execute('DELETE FROM produtos WHERE id = ?', (id,))
        conn.commit()
        conn.close()

        registrar_historico(f"Produto '{nome_produto}' foi REMOVIDO.")
        return jsonify({'message': 'Produto deletado!'})
    except Exception as e:
        return jsonify({'message': str(e)}), 500

# Histórico
def registrar_historico(mensagem):
    conn = sqlite3.connect('estoque.db')
    cursor = conn.cursor()
    data_atual = datetime.now().strftime("%d/%m/%Y %H:%M")
    cursor.execute('INSERT INTO historico (mensagem, data_hora) VALUES (?, ?)', (mensagem, data_atual))
    conn.commit()
    conn.close()

@app.route('/api/historico', methods=['GET'])
def get_historico():
    conn = sqlite3.connect('estoque.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM historico ORDER BY id DESC LIMIT 10')
    historico = cursor.fetchall()
    conn.close()
    return jsonify(historico)

if __name__ == '__main__':
    app.run(debug=True)