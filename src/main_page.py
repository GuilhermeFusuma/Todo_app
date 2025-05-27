import flet as ft
from cores import cores
from componentes import *
import todo_db as db

class LeftMenu(ft.Container):
    def __init__(self, app: ft.Row):
        super().__init__()
        self.app = app
        # lista com tuplas contendo o id e o título da página    
        self.paginas = db.get_paginaids()


        # Configurações do container
        self.padding = 10
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
            expand=True,
            scroll=True,
            controls=[BotaoPagina(lambda e, id=pagina["id"]: self.app.switch_page(id), pagina["titulo"], pagina["id"], self) for pagina in self.paginas]
        )

        # Conteúdo do menu
        self.conteudo = ft.Column(
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
                self.pages,
                ft.Container(
                    content=ft.IconButton(
                        icon=ft.Icons.ADD,
                        bgcolor=cores["fore2"],
                        icon_color=cores["fore1"],
                        icon_size=30,
                        on_click=lambda e: self.add_page(),
                    ),
                    padding=10
                )
            ]
        )
        
        self.content = self.conteudo

    def add_page(self):
        main_page = self.app.controls[1] #main page para adicionar a tela de criação

        def verificar(titulo):
            db.add_pagina(titulo, "tarefas")

            main_page.content.controls.remove(container_criar) # remove a janela da página a mostra
            main_page.update()
            self.att_paginas() # Atualiza as páginas neste container

        campo_texto = ft.TextField(
            label="Título",
        )

        def fechar():
            main_page.content.controls.remove(container_criar)
            main_page.update()

        container_criar = ft.Container(
            bgcolor="#80000000",
            expand=True,
            alignment=ft.alignment.center,
            on_click=lambda e: fechar(),
            content=ft.Container(
                bgcolor=cores["bg2"],
                padding=40,
                width= 300,
                height=180,
                border_radius=10,
                shadow=ft.BoxShadow(blur_radius=4, color=ft.Colors.BLACK, offset=ft.Offset(-4, 4)),
                on_click=lambda e: None,
                content=ft.Column(
                    controls=[
                        campo_texto,
                        ft.Button(
                            text="Criar página",
                            bgcolor=cores["fore2"],
                            color=cores["fore1"],
                            on_click=lambda e: verificar(campo_texto.value)
                        )
                    ],
                    alignment=ft.MainAxisAlignment.END
                )
            )
        )

        if len(main_page.content.controls) < 2:
            main_page.content.controls.append(container_criar)
            main_page.update()

    def att_paginas(self):
        self.paginas = db.get_paginaids()  # Atualiza as páginas no banco
        self.pages.controls.clear()  # Limpa os botões antigos

        # Cria novos botões
        for pagina in self.paginas:
            botao = BotaoPagina(
                lambda e, id=pagina["id"]: self.app.switch_page(id),
                pagina["titulo"],
                pagina["id"],
                self
            )
            self.pages.controls.append(botao)
        self.app.get_paginas() # Atualiza as páginas existentes no app

        self.pages.update()  # Atualiza o container que é visível        

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
            self.content= self.conteudo

            self.mini = False

        self.app.update()

class Chat_Menu(ft.Container):
    def __init__(self, app: ft.Row):
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

class Main_Page(ft.Container):
    def __init__(self, titulo, app: ft.Row, id_pagina):
        super().__init__()
        self.titulo = titulo
        self.expand = True
        self.padding = 20
        self.bgcolor = cores["bg1"]
        self.app = app

        self.id = id_pagina
        self.datas = []
        self.tarefas_por_data = {}

        # coluna que organiza os containeres das tarefas
        self.tarefas_body = ft.Column(
            expand=True,
            scroll="auto"
        )

        def editar_titulo(novo_titulo):
            self.titulo = novo_titulo
            db.edit_pagina(self.id, novo_titulo, "tarefa")

            self.update() # Atualiza a página
            self.app.left_menu.att_paginas()

        self.conteudo = ft.Stack(
            controls=[
                ft.Column(
                    controls=[

                        ft.Row( # Header da página
                            controls=[
                                LabelEditavel(self.titulo, "str", scale=3.5, on_submit=lambda value: editar_titulo(value)),
                                ft.FloatingActionButton(
                                    bgcolor=cores["fore2"],
                                    foreground_color=cores["fore1"],
                                    icon=ft.Icons.ADD,
                                    on_click=lambda e: self.criar_tarefa()
                                )
                            ],
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                        ),

                        self.tarefas_body
                    ],
                    spacing = 15
                )
            ],
            expand=True,
            alignment=ft.alignment.center
        )

        # Conteúdo
        self.content = self.conteudo

    def criar_tarefa(self):
        titulo = ft.TextField(
            label="Titulo",
        )
        data_termino = ft.TextField(
            label="Data de término",
            hint_text="--/--/----",
        )

        def fechar():
            self.conteudo.controls.pop(1)
            self.update()

        # Verifica os dados
        def verificar():
            titulo_valido = False
            data_valido = False

            if len(titulo.value.strip()) > 0: # verifica se tem texto no campo
                titulo_valido = True
            
            try: # verifica se a data é válida
                datetime.strptime(data_termino.value,"%d/%m/%Y")
                data_valido = True
            except ValueError:
                data_valido = False

            if titulo_valido and data_valido: # Se ambos os campos forem válidos, adiciona no banco de dados e atualiza a página
                db.add_tarefa(
                    titulo.value,
                    datetime.now().date().strftime("%d/%m/%Y"),
                    data_termino.value,
                    self.id
                )

                self.conteudo.controls.remove(container_criar)
                self.update()

                self.consultar_tarefas()
            elif not titulo_valido:
                titulo.focus()
            elif not data_valido:
                data_termino.focus()

        container_criar = ft.Container(
            expand=True,
            bgcolor= "#80000000",
            alignment=ft.alignment.center,
            on_click=lambda e: fechar(),
            content=ft.Container(
                bgcolor=cores["bg2"],
                padding=15,
                border_radius=20,
                shadow=ft.BoxShadow(blur_radius=7, color=ft.Colors.BLACK, offset=ft.Offset(-2.0, 2.0)),
                on_click=lambda e: None,
                content=ft.Column(
                    controls=[
                        titulo,
                        data_termino,
                        ft.Button(
                            text="Criar tarefa",
                            on_click=lambda e: verificar(),
                            bgcolor=cores["fore2"],
                            color=cores["fore1"],
                        )
                    ],
                    height=300,
                    width=270,
                    horizontal_alignment=ft.CrossAxisAlignment.END,
                    alignment=ft.MainAxisAlignment.SPACE_AROUND
                )
            )
        )

        if len(self.conteudo.controls) < 2:
            self.conteudo.controls.append(container_criar)
        self.update()

    def consultar_tarefas(self):
        tarefas = db.tarefas_por_pagina(self.id)

        # Reseta os dados
        self.datas = []
        self.tarefas_por_data = {}
        self.tarefas_body.controls.clear()

        # Organização
        for tarefa in tarefas: # cria uma lista com todas as datas
            if tarefa["data_de_termino"] not in self.datas:
                self.datas.append(tarefa["data_de_termino"])
       
        for data in self.datas: # organiza o dicionário para armazenar as tarefas por data
            temp_list = []
            for tarefa in tarefas:
                if tarefa["data_de_termino"] == data:
                    temp_list.append(tarefa)
        
            self.tarefas_por_data.setdefault(data, temp_list)

        # Adiciona as tarefas no conteúdo
        for data in self.datas:
            tars = self.tarefas_por_data[data]

            self.tarefas_body.controls.append(ContainerTarefas(data, tars, self))

        self.update()

    def att_datas(self):
        for container in self.tarefas_body.controls:
            if not len(container.tarefas.controls):
                self.tarefas_body.controls.remove(container)
        
        self.update()

class TodoApp(ft.Row):
    def __init__(self, page):
        super().__init__()
        self.page = page

        self.func = None
        self.get_paginas()

        # janelas
        self.left_menu = LeftMenu(self)
        self.chat_menu = Chat_Menu(self)

        #config
        self.spacing = 0
        self.expand = True

        self.controls = [
            self.left_menu,
            self.paginas[self.ids[0]],
            # self.chat_menu
        ]

    def get_paginas(self):
        paginas = db.get_paginas()
        self.paginas = {}

        # Organiza as páginas
        for pagina in paginas:
            self.paginas.setdefault(
                pagina["id"], 
                Main_Page(
                    pagina["titulo"],
                    self, 
                    pagina["id"]
                )
            )

            self.ids = list(self.paginas.keys())
            # self.id_titulos = [(pagina["id"], pagina["titulo"]) for pagina in self.ids]

    def get_func(self, fn):
        self.func = fn

    def switch_page(self, id): # troca de páginas
        self.controls.pop(1)
        self.controls.insert(1, self.paginas[id])
        self.update()
        self.paginas[id].consultar_tarefas()
