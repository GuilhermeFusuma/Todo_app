import flet as ft
from cores import cores
from componentes import *

class LeftMenu(ft.Container):
    def __init__(self, page):
        super().__init__()
        # Configurações do container
        self.padding = 5
        self.bgcolor = cores["bg2"]
        self.width = 300
        self.height = page.height
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
                ),
                ft.Column(
                    controls=[
                        ft.Text('Teste')
                    ]
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

class Chat_Menu(ft.Container):
    def __init__(self, page):
        super().__init__()
        self.padding = 5
        self.mini = True
        self.width = 50
        self.bgcolor = cores["bg2"]
        self.height = page.height
        self.arrow = ArrowButton(self.toggle_chat)

        self.open_width = min(300, page.width*0.3)

        # Chat de conversa (ficará escondido no início)
        self.chat = Chat()

        # Seta para abrir a aba
        self.content = self.arrow
        self.alignment = ft.Alignment(0.0, 0.0)
    
    def toggle_chat(self, e):
        if not self.mini: # Caso não esteja minimizada
            self.arrow.rotate = 0 
            self.content = self.arrow
            self.width = 50

            self.mini = True 
        elif self.mini: # Caso esteja minimizada
            self.width = self.open_width
            self.arrow.rotate = 3.14 # Rotaciona um radiano
            self.content= ft.Column(
                controls=[
                    ft.Row(
                        controls=[
                            self.arrow
                        ]
                    ),
                    self.chat
                ],
                spacing=20,
                
            )

            self.mini = False

        self.update()

class Chat(ft.Container):
    def __init__(self):
        super().__init__()
        self.expand = True
        self.width = 300
        self.bgcolor = cores["bg1"]
        self.padding = 5
        self.alignment = ft.Alignment(0.0, 1.0)

        self.campo_mensagens = ft.Column(
            expand=True,
            scroll=ft.ScrollMode.AUTO
        )
        self.campo_texto = ft.TextField(on_submit=self.enviar)

        # Parte de conversa
        self.content = ft.Column(
            controls=[
                self.campo_mensagens,
                ft.Row(
                    controls=[
                        ft.Container(
                            bgcolor=cores["bg2"],
                            expand=True,
                            content=self.campo_texto,
                            
                        ),
                        ft.Container(
                            content=ft.Icon(name=ft.Icons.SEND, color=cores["fore1"]),
                            on_click=self.enviar
                        )
                    ],
                    spacing=10
                )
            ]
        )

    def enviar(self, e):
        if len(self.campo_texto.value) > 0:
            self.campo_mensagens.controls.append(
                Balao(self.campo_texto.value)
            )
            self.campo_mensagens.update()

        # Limpa o campo de texto
        self.campo_texto.value = ""
        self.campo_texto.update()
        self.campo_texto.focus()


class TodoApp(ft.Row):
    def __init__(self, page):
        super().__init__()
        self.left_menu = LeftMenu(page)
        self.chat_menu = Chat_Menu(page)

        self.controls = [
            self.left_menu,
            ft.Container(
                width=page.width/2 - (self.left_menu.width + self.chat_menu.width),
                height=page.height,
                bgcolor="FF0000",
                content=ft.Text("teste")
            ),
            self.chat_menu
        ]

        print(self.controls)

    #TODO: corrigir essa função que não funciona
    def resize_update(self, e):
        self.left_menu.height = 500
        self.left_menu.update()
      