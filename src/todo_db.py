import sqlite3 as sql

# criando connection e cursor
conn = sql.connect("todo_app.db")

# usado para interagir com o banco de dados
cursor = conn.cursor()

# Cria a tabela de páginas
cursor.execute("""
CREATE TABLE IF NOT EXISTS paginas(
    id_pagina INTEGER PRIMARY KEY AUTOINCREMENT, 
    titulo TEXT, 
    tipo TEXT
)""" )

# Cria a tabela de tarefas
cursor.execute("""
CREATE TABLE IF NOT EXISTS tarefas (
    id_tarefa INTEGER PRIMARY KEY AUTOINCREMENT,
    titulo TEXT,
    descricao TEXT,
    categoria TEXT,
    prioridade INTEGER,
    data_de_criacao TEXT,
    data_de_termino TEXT,
    id_pagina INTEGER,
    FOREIGN KEY(id_pagina) REFERENCES paginas(id_pagina)
)
""")

#-------------- funções para interagir com o banco de dados----------------------

def add_pagina(titulo, tipo):
    cursor.execute("INSERT INTO paginas (titulo, tipo) VALUES (?, ?)", (titulo, tipo))
    conn.commit()

def add_tarefa(titulo, descricao, prioridade, data_cri, data_term, id_pag):
    cursor.execute("INSERT INTO tarefas (titulo, descricao, categoria, prioridade, data_de_criacao, data_de_termino, id_pagina) VALUES (?, ?, ?, ?, ?, ?))", (titulo, descricao, prioridade, data_cri, data_term, id_pag))
    conn.commit()

add_pagina("teste", "tarefas")

