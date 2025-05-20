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
    finalizado INTEGER,
    id_pagina INTEGER,
    FOREIGN KEY(id_pagina) REFERENCES paginas(id_pagina)
)
""")

cursor.execute("SELECT * FROM paginas")
result = cursor.fetchall()
if not len(result):
    cursor.execute("""
    INSERT INTO paginas (titulo, tipo) VALUES ("Lista de tarefas (teste base)", "tarefa")
    """)

# cursor.execute("SELECT * FROM paginas")
# print(cursor.fetchall())

#-------------- funções para interagir com o banco de dados----------------------

def add_pagina(titulo, tipo):
    cursor.execute("INSERT INTO paginas (titulo, tipo) VALUES (?, ?)", (titulo, tipo))
    conn.commit()
def add_tarefa(titulo, descricao, prioridade, data_cri, data_term, id_pag):
    cursor.execute("INSERT INTO tarefas (titulo, descricao, categoria, prioridade, data_de_criacao, data_de_termino, id_pagina) VALUES (?, ?, ?, ?, ?, ?))", (titulo, descricao, prioridade, data_cri, data_term, id_pag))
    conn.commit()

def delete_pagina(id):
    cursor.execute("DELETE FROM paginas WHERE id_pagina = ?", (id))
    conn.commit()
def delete_tarefa(id):
    cursor.execute("DELETE FROM tarefas WHERE id_tarefa = ?", (id))
    conn.commit()


def get_paginas():
    cursor.execute("SELECT * FROM paginas")
    return cursor.fetchall()
def get_tarefas(id_pagina):
    cursor.execute("SELECT * FROM tarefas WHERE id_pagina = ?", (id_pagina)) 
    return cursor.fetchall()

def get_pagina_id(id):
    cursor.execute("SELECT * from paginas WHERE id_pagina = ?", (id))
    return cursor.fetchall()
def get_tarefa_id(id):
    cusor.execute("SELECT * FROM tarefas WHERE id_tarefa = ?", (id))
    return cursor.fetchall()


def edit_pagina(id, titulo, tipo):
    cursor.execute("UPDATE paginas SET titulo = ?, tipo = ? WHERE id_pagina = ?", (titulo, tipo, id))
    conn.commit()
def edit_tarefa(id, titulo, descricao, prioridade, data_term):
    cursor.execute("UPDATE tarefas SET titulo = ?, descricao = ?, prioridade = ?, data_termino = ? WHERE id_tarefa = ?", (titulo, descricao, prioridade, data_term, id))
    conn.commit()
