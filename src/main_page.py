import flet as ft
from cores import cores
from componentes import *



class LeftMenu(ft.Container):
    def __init__(self, page, app: ft.Row, titulos):
        super().__init__()
        self.app = app
        self.titulos = titulos # lista com tuplas contendo o id e o título da página

        # Configurações do container
        self.padding = 5
        self.bgcolor = cores["bg2"]
        self.width = 300
        self.temp_animacao = 500
        self.animate = ft.Animation(duration=self.temp_animacao, curve=ft.AnimationCurve.EASE_IN_OUT)
        self.mini = False # Variável de controle para checar se está minimizado ou não

        # Conteúdo do container
        self.arrow = ArrowButton(self.toggle_menu)
        self.arrow.rotate = 3.14 # rotaciona 1 radiano

        self.paginas_container = ft.Column()

        self.pages = ft.Column(
            controls=[BotaoPagina(lambda e, id=id: app.switch_page(id), titulo) for id, titulo in self.titulos]
        )

        # Cria as páginas
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
                self.pages
            ]
        )

    # Modifica o estado do menu à esquerda entre minimizado e normal
    def toggle_menu(self, e):
        if not self.mini: # minimizar
            self.arrow.rotate = 0
            self.content = ft.Column(
                controls=[
                    self.arrow
                ],
            )
            self.width = 50
            self.alignment = ft.alignment.center

            self.mini = True 
        elif self.mini: # Caso esteja minimizada
            self.width = 300
            self.arrow.rotate = 3.14
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

        self.app.update()

class Chat_Menu(ft.Container):
    def __init__(self, page, app: ft.Row):
        super().__init__()
        self.app = app
        self.padding = 5
        self.mini = True
        self.width = 50
        self.bgcolor = cores["bg2"]

        # animação
        self.animate = ft.Animation(duration=250, curve=ft.AnimationCurve.EASE_IN_OUT)

        self.arrow = ArrowButton(self.toggle_chat)
        self.arrow.rotate = 3.14

        self.chat = Chat()
        self.content = self.arrow
        self.alignment = ft.Alignment(0.0, 0.0)

    def toggle_chat(self, e):
        if not self.mini:
            self.arrow.rotate = 3.13
            self.content = self.arrow
            self.width = 50
            self.mini = True
        else:
            self.arrow.rotate = 0
            self.content = ft.Column(
                controls=[
                    ft.Row(controls=[self.arrow]),
                    self.chat
                ],
                spacing=20
            )
            self.width = 300
            self.mini = False

        self.app.update()

class Chat(ft.Container):
    def __init__(self):
        super().__init__()
        self.expand = True
        self.bgcolor = cores["bg1"]
        self.padding = 5
        self.alignment = ft.Alignment(0.0, 1.0)

        self.campo_mensagens = ft.ListView(
            expand=True,
            auto_scroll=True,
            spacing = 10
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
                ft.Row(
                    controls=[
                        Balao(self.campo_texto.value)
                    ],
                    alignment=ft.CrossAxisAlignment.END,
                    width=200
                )
            )
            self.campo_mensagens.update()

        # Limpa o campo de texto
        self.campo_texto.value = ""
        self.campo_texto.update()
        self.campo_texto.focus()

class Main_Menu(ft.Container):
    def __init__(self, titulo, page, app: ft.Row, tarefas):
        super().__init__()
        self.expand = True
        self.padding = 20

        self.tarefas = tarefas
        self.datas = []
        self.tarefas_por_data = {}

        # Organização
        for tarefa in self.tarefas: # cria uma lista com todas as datas
            if tarefa["data_de_termino"] not in self.datas:
                self.datas.append(tarefa["data_de_termino"])
       
        for data in self.datas: # organiza o dicionário para armazenar as tarefas por data
            temp_list = []
            for tarefa in self.tarefas:
                if tarefa["data_de_termino"] == data:
                    temp_list.append(tarefa)
        
            self.tarefas_por_data.setdefault(data, temp_list)

        # coluna que organiza os containeres das tarefas
        self.tarefas_body = ft.Column(
            expand=True,
            scroll="auto"
        )

        # Conteúdo
        self.content = ft.Column(
            controls=[
                ft.Row(
                    controls=[
                        ft.Text(titulo, size = 35)
                    ]
                ),
                self.tarefas_body
            ],
            spacing = 15
        )

        # Adiciona as tarefas no conteúdo
        for data in self.datas:
            tarefas = self.tarefas_por_data[data]

            self.tarefas_body.controls.append(ContainerTarefas(data, tarefas))

    # def get_data

class TodoApp(ft.Row):
    def __init__(self, page):
        super().__init__()

        # teste (esses dados devem ser recebidos neste formato depois)
        tarefas = [
            {
                'id': 1,
                'titulo': 'tarefa_teste',
                'descricao': 'descricao para teste',
                'categoria': '',
                'prioridade': 1,
                'data_de_criacao': '20/05/2025',
                'data_de_termino': '22/05/2025',
                'finalizado': 0,
                'id_pagina': 1
            },
            {
                'id': 3,
                'titulo': 'tarefa_teste',
                'descricao': 'descricao para teste',
                'categoria': '',
                'prioridade': 1,
                'data_de_criacao': '20/05/2025',
                'data_de_termino': '22/05/2025',
                'finalizado': 0,
                'id_pagina': 1
            },
            {
                'id': 3,
                'titulo': 'tarefa_teste',
                'descricao': 'descricao para teste',
                'categoria': '',
                'prioridade': 1,
                'data_de_criacao': '20/05/2025',
                'data_de_termino': '22/05/2025',
                'finalizado': 0,
                'id_pagina': 2
            },
            {
                'id': '2',
                'titulo': 'tarefa_teste2',
                'descricao': 'descricao para teste',
                'categoria': '',
                'prioridade': 1,
                'data_de_criacao': '20/05/2025',
                'data_de_termino': '23/05/2025',
                'finalizado': 0,
                'id_pagina': 2
            },
            {
                'id': '5',
                'titulo': 'tarefa_teste2',
                'descricao': 'descricao para teste',
                'categoria': '',
                'prioridade': 1,
                'data_de_criacao': '20/05/2025',
                'data_de_termino': '23/05/2025',
                'finalizado': 0,
                'id_pagina': 1
            }
        ]

        paginas = [
            {
                "id": 1,
                "titulo": 'titulo_teste',
                "tipo": "tipo"
            },
            {
                "id": 2,
                "titulo": 'titulo_teste 2',
                "tipo": "tipo"
            },
        ]

        self.tarefas_por_idpagina = {}

        for tarefa in tarefas:
            if self.tarefas_por_idpagina.get(tarefa["id_pagina"]):
                self.tarefas_por_idpagina[tarefa["id_pagina"]].append(tarefa)
            else:
                self.tarefas_por_idpagina.setdefault(tarefa["id_pagina"], [tarefa])

        print(self.tarefas_por_idpagina)

        # eu vou precisar transformar depois os dados do banco de dados para chegar aqui
        self.paginas = {}

        # Organiza as páginas
        for pagina in paginas:
            print(pagina)
            self.paginas.setdefault(
                pagina["id"], 
                Main_Menu(
                    f"Página {pagina["id"]}", 
                    page, 
                    self, 
                    self.tarefas_por_idpagina[pagina["id"]] if self.tarefas_por_idpagina.get(pagina["id"]) else []
                )
            )

        self.ids = list(self.paginas.keys())
        self.id_titulos = [(pagina["id"], pagina["titulo"]) for pagina in paginas]

        # janelas
        self.left_menu = LeftMenu(page, self, self.id_titulos)
        self.chat_menu = Chat_Menu(page, self)

        #config
        self.spacing = 0
        self.expand = True

        self.controls = [
            self.left_menu,
            self.paginas[self.ids[0]],
            self.chat_menu
        ]

    def switch_page(self, id): # troca de páginas
        self.controls.pop(1)
        self.controls.insert(1, self.paginas[id])
        self.update()
