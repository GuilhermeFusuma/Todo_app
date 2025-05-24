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

conn.commit()
conn.close()

#-------------- funções para interagir com o banco de dados----------------------

# É melhor criar a conexão para cada função para que não ocorra erro de threads

def add_pagina(titulo, tipo):
    conn = sql.connect("todo_app.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO paginas (titulo, tipo) VALUES (?, ?)", (titulo, tipo))
    conn.commit()
    conn.close()
def add_tarefa(titulo, data_cri, data_term, fin, id_pag, descricao='', categoria='', prioridade=0):
    conn = sql.connect("todo_app.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO tarefas (titulo, descricao, categoria, prioridade, data_de_criacao, data_de_termino, finalizado, id_pagina) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", (titulo, descricao, categoria, prioridade, data_cri, data_term, fin, id_pag))
    conn.commit()
    conn.close()

def delete_pagina(id):
    conn = sql.connect("todo_app.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM paginas WHERE id_pagina = (?)", (id,))
    conn.commit()
    conn.close()
def delete_tarefa(id):
    conn = sql.connect("todo_app.db")
    cursor = conn.cursor()

    cursor.execute("DELETE FROM tarefas WHERE id_tarefa = ?", (id,))
    conn.commit()
    conn.close()

    print(f'tarefa com id {id} deletada')

def get_paginas(): # função que retorna todas as páginas do bd
    conn = sql.connect("todo_app.db")
    cursor = conn.cursor()
    paginas = []

    cursor.execute("SELECT * FROM paginas")
    # organiza as páginas para enviar para o front
    for pagina in cursor.fetchall():
        paginas.append({
            "id": pagina[0],
            "titulo": pagina[1],
            "tipo": pagina[2]
        })

    conn.close()
    return paginas

def get_tarefas(): # função que retorna todas as tarefas do bd
    conn = sql.connect("todo_app.db")
    cursor = conn.cursor()

    tarefas = []

    cursor.execute("SELECT * FROM tarefas")
    for tarefa in cursor.fetchall():
        tarefas.append({
            "id": tarefa[0],
            "titulo": tarefa[1],
            "descricao": tarefa[2],
            "categoria": tarefa[3],
            "prioridade": tarefa[4],
            "data_de_criacao": tarefa[5],
            "data_de_termino": tarefa[6],
            "finalizado": tarefa[7],
            "id_pagina": tarefa[8]
        })

    conn.close()
    return tarefas

# Não sei se será usado
def get_pagina_id(id):
    conn = sql.connect("todo_app.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * from paginas WHERE id_pagina = ?", (id,))
    
    conn.close()
    

def get_tarefa_id(id):
    conn = sql.connect("todo_app.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tarefas WHERE id_tarefa = ?", (id,))
    
    
    tarefa = cursor.fetchall()[0]
    tarefa_dict = {
            "id": tarefa[0],
            "titulo": tarefa[1],
            "descricao": tarefa[2],
            "categoria": tarefa[3],
            "prioridade": tarefa[4],
            "data_de_criacao": tarefa[5],
            "data_de_termino": tarefa[6],
            "finalizado": tarefa[7],
            "id_pagina": tarefa[8]
        }
    conn.close()
    return tarefa_dict

def get_paginaids():
    conn = sql.connect("todo_app.db")
    cursor = conn.cursor()

    paginas = []
    cursor.execute("SELECT id_pagina, titulo FROM paginas")
    for pagina in cursor.fetchall():
        paginas.append({
            "id": pagina[0],
            "titulo": pagina[1]
        })
    
    conn.close()
    return paginas


def edit_pagina(id, titulo, tipo):
    conn = sql.connect("todo_app.db")
    cursor = conn.cursor()

    cursor.execute("UPDATE paginas SET titulo = ?, tipo = ? WHERE id_pagina = ?", (titulo, tipo, id))
    conn.commit()
    conn.close()
def edit_tarefa(id, titulo, descricao, prioridade, data_term):
    conn = sql.connect("todo_app.db")
    cursor = conn.cursor()

    cursor.execute("UPDATE tarefas SET titulo = ?, descricao = ?, prioridade = ?, data_de_termino = ? WHERE id_tarefa = ?", (titulo, descricao, prioridade, data_term, id))
    conn.commit()
    conn.close()

def check_tarefa(id, value: bool = True):
    conn = sql.connect("todo_app.db")
    cursor = conn.cursor()

    check = 1 if value else 0
    cursor.execute("UPDATE tarefas SET finalizado = ? WHERE id_tarefa = ?", (check, id))
    conn.close()