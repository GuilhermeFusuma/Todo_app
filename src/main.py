import flet as ft
from cores import cores
import todo_db as bd
from main_page import TodoApp

def main(page: ft.Page):
    page.title = "Todo app"
    page.padding = 0

    app = TodoApp(page)

    page.add(app)

    app.paginas[app.ids[0]].consultar_tarefas()

    def resize(e):
        print('mudou de tamanho')

    page.on_resize = resize

ft.app(target=main)