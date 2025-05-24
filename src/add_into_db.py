import sqlite3 as sql
import todo_db as db

# criando connection e cursor
conn = sql.connect("todo_app.db")

# usado para interagir com o banco de dados
cursor = conn.cursor()

db.add_pagina("Pessoal", "tarefas")
cursor.execute("""
INSERT INTO tarefas 
(titulo, descricao, categoria, prioridade, data_de_criacao, data_de_termino, finalizado, id_pagina)
VALUES
('Tarefa1', 'descrição teste', 'categoria', 1, '22/05/2025', '23/06/2025', 0, 1)
""")
cursor.execute("""
INSERT INTO tarefas 
(titulo, descricao, categoria, prioridade, data_de_criacao, data_de_termino, finalizado, id_pagina)
VALUES
('Tarefa2', 'descrição teste', 'categoria', 1, '22/05/2025', '27/06/2025', 0, 2)
""")
cursor.execute("""
INSERT INTO tarefas 
(titulo, descricao, categoria, prioridade, data_de_criacao, data_de_termino, finalizado, id_pagina)
VALUES
('Tarefa3', 'descrição teste', 'categoria', 1, '22/05/2025', '26/06/2025', 0, 2)
""")
cursor.execute("""
INSERT INTO tarefas 
(titulo, descricao, categoria, prioridade, data_de_criacao, data_de_termino, finalizado, id_pagina)
VALUES
('Tarefa4', 'descrição teste', 'categoria', 1, '22/05/2025', '26/06/2025', 0, 2)
""")
conn.commit()

conn.close()