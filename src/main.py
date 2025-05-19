import flet as ft
from cores import cores
import todo_db as bd
from main_page import TodoApp

def main(page: ft.Page):
    page.title = "Todo app"
    page.padding = 0

    app = TodoApp(page)

    page.add(app)
    page.on_resize = app.update()

ft.app(target=main)