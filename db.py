import sqlite3
from datetime import datetime

# Função auxiliar para conectar 
def get_connection():
    return sqlite3.connect('estoque.db')

def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    # Criação da tabela de produtos
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

def registrar_historico(mensagem):
    conn = get_connection()
    cursor = conn.cursor()
    data_atual = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    cursor.execute('INSERT INTO historico (mensagem, data_hora) VALUES (?, ?)', (mensagem, data_atual))
    conn.commit()
    conn.close()

def listar_historico():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM historico ORDER BY id DESC LIMIT 10')
    historico = cursor.fetchall()
    conn.close()
    return historico