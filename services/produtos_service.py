import  sqlite3
from db import get_connection, registrar_historico

def listar_produtos(categoria=None):
    conn = get_connection()
    cursor = conn.cursor()
    
    if categoria:
        cursor.execute('SELECT * FROM produtos WHERE categoria = ?', (categoria,))
    else:
        cursor.execute('SELECT * FROM produtos')
    produtos = cursor.fetchall()
    conn.close()
    return produtos

def criar_produto(data):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO produtos (codigo, nome, quantidade, preco, categoria, tamanho)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (data['codigo'], data['nome'], data['quantidade'], data['preco'], data.get('categoria'), data.get('tamanho')))
        conn.commit()
        conn.close()
        registrar_historico(f"[{data['categoria'].upper()}] Produto '{data['nome']}' criado.")
        return {"success": True, "message": "Produto Adicioando!."}
    
    except sqlite3.IntegrityError:
        return {"success": False, "message": "Erro: Produto com este código já existe na categoria."}
    except Exception as e:
        return {"success": False, "message": str(e)}
    

def editar_produto(produto_id, data):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        # Busca dados antigos
        cursor.execute('SELECT * FROM produtos WHERE id = ?', (produto_id,))
        produto_atual = cursor.fetchone()

        if not produto_atual:
            return {"success": False, "message": "Produto não encontrado."}
        
        antigo_nome = produto_atual[2]
        antigo_qtd = produto_atual[3]
        antigo_preco = produto_atual[4]


        # Define novos produtos
        novo_codigo = data.get('codigo') or produto_atual[1]
        novo_nome = data.get('nome') or produto_atual[2]
        novo_qtd = data.get('quantidade') or produto_atual[3]
        novo_preco = data.get('preco') or produto_atual[4]
        novo_categoria = data.get('categoria') or produto_atual[5]
        novo_tamanho = data.get('tamanho') or produto_atual[6]

        # Detectar mudanças
        alteracoes = []
        if novo_nome != antigo_nome:
            alteracoes.append(f"Nome: '{antigo_nome}' -> '{novo_nome}'")
        if float(novo_qtd) != float(antigo_qtd):
            alteracoes.append(f"Quantidade: {antigo_qtd} -> {novo_qtd}")
        if float(novo_preco) != float(antigo_preco):
            alteracoes.append(f"Preço: {antigo_preco} -> {novo_preco}")

        # Atualiza o produto no banco de dados
        cursor.execute('''
            UPDATE produtos
            SET codigo = ?, nome = ?, quantidade = ?, preco = ?, categoria = ?, tamanho = ?
            WHERE id = ?
        ''', (novo_codigo, novo_nome, novo_qtd, novo_preco, novo_categoria, novo_tamanho, produto_id))

        conn.commit()
        conn.close()

        if alteracoes:
            mensagem_detalhada = f"Produto '{novo_nome}' editado. Mudanças: " + " | ".join(alteracoes)
            registrar_historico(mensagem_detalhada)
        else:
            registrar_historico(f"Produto '{novo_nome}' editado sem mudanças.")

        return {"success": True, "message": "Produto atualizado com sucesso."}
    except Exception as e:
        return {"success": False, "message": str(e)}    
    

def removerProduto(produto_id):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute('SELECT nome FROM produtos WHERE id = ?', (produto_id,))
        produto = cursor.fetchone()
        nome_produto = produto[0] if produto else "Desconhecido"

        cursor.execute('DELETE FROM produtos WHERE id = ?', (produto_id,))
        conn.commit()   
        conn.close()

        registrar_historico(f"Produto '{nome_produto}' removido do estoque.")
        return {"success": True, "message": "Produto removido com sucesso."}
    except Exception as e:
        return {"success": False, "message": str(e)}
    
