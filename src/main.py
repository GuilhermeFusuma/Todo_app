import flet as ft
from cores import cores
import todo_db as bd

# botão flecha que executa uma função passada nos argumentos
class ArrowButton(ft.IconButton):
    def __init__(self, func):
        super().__init__()
        self.icon = ft.Icons.ARROW_BACK
        self.icon_color = cores["fore1"]
        self.icon_size = 20

        self.on_click = func

class LeftMenu(ft.Container):
    def __init__(self, page):
        super().__init__()
        # Configurações do container
        self.padding = 5
        self.bgcolor = cores["bg2"]
        self.width = 300
        self.height = page.height
        self.alignment=ft.Alignment(0.0, -1.0)
        self.temp_animacao = 500
        self.animate = ft.Animation(duration=self.temp_animacao, curve=ft.AnimationCurve.EASE_IN_OUT)
        self.mini = False # Variável de controle para checar se está minimizado ou não

        # Conteúdo do container
        self.arrow = ArrowButton(self.toggle_menu)

        self.content= ft.Column(
            controls=[
                ft.Row(
                    controls=[
                        ft.Text(
                            "Todo App",
                            weight="bold",
                            size=35,
                            color=cores["fore1"],
                            ),
                        self.arrow
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    vertical_alignment= ft.CrossAxisAlignment.CENTER,
                )
            ]
        )

    # Modifica o estado do menu à esquerda entre minimizado e normal
    def toggle_menu(self, e):
        if not self.mini: # Caso não esteja minimizada
            self.arrow.rotate = 3.14 # Rotaciona um radiano
            self.content = ft.Column(
                controls=[
                    self.arrow
                ],
                alignment=ft.Alignment(0.0, 0.0),
                height=self.height
            )
            self.width = 50
            self.alignment = ft.Alignment(0.0, 0.0)

            self.mini = True 
        elif self.mini: # Caso esteja minimizada
            self.width = 300
            self.arrow.rotate = 0
            self.content= ft.Column(
                controls=[
                    ft.Row(
                        controls=[
                            ft.Text("Todo App", weight="bold", size=35, color=cores["fore1"]),
                            self.arrow
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        vertical_alignment= ft.CrossAxisAlignment.CENTER,
                    )
                ]
            )

            self.mini = False

        self.update()

class TodoApp(ft.Row):
    def __init__(self, page):
        super().__init__()
        self.left_menu = LeftMenu(page)
        self.chat = ft.Container(
            padding=10,
            bgcolor=cores["bg2"],
            width=50
        )

        self.controls = [
            self.left_menu
        ]

    #TODO: corrigir essa função que não funciona
    def resize_update(self, e):
        self.left_menu.height = self.page.height
        self.left_menu.update()
        

def main(page: ft.Page):
    page.title = "Todo app"
    page.padding = 0

    app = TodoApp(page)

    page.add(app)
    page.on_resize = app.resize_update

ft.app(target=main)