import flet as ft
from componentes import LabelEditavel, InfoTarefa
import todo_db as db

def main(page: ft.Page):
    page.title = "Teste"

    tarefa = db.get_tarefa_id(2)

    app = InfoTarefa(tarefa["id"], tarefa["titulo"], tarefa["descricao"], tarefa["data_de_criacao"], tarefa["data_de_termino"], tarefa["prioridade"], tarefa["categoria"], tarefa["id_pagina"])

    page.add(app)

ft.app(target=main)
