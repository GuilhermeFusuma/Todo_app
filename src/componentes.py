import flet as ft
from cores import cores
import todo_db as db
from datetime import datetime

# botão flecha que executa uma função passada nos argumentos
class ArrowButton(ft.IconButton):
    def __init__(self, func):
        super().__init__()
        self.icon = ft.Icons.ARROW_FORWARD_IOS
        self.icon_color = cores["fore1"]
        self.icon_size = 20

        self.on_click = func

class MyIconBtn(ft.Container):
    def __init__(self, img_path, func, scale):
        super().__init__()
        self.func = func
        self.width = 30 * scale
        self.height = 30 * scale
        self.opacity = 0.4

        self.on_click = self.func

        self.content = ft.Image(
            src=img_path,
            width=self.width,
            height=self.height,
            fit=ft.ImageFit.CONTAIN
        )

        def on_hover(e):
            self.opacity = 1.0 if e.data == "true" else  0.4
            self.update()

        self.on_hover = on_hover

# Balão para o chat
class Balao(ft.Container):
    def __init__(self, texto, agente="user"):
        super().__init__()

        self.bgcolor = cores["bg2"]
        self.padding = 10
        self.border_radius = 10
        self.content = ft.Row(
            controls=[
                ft.Text(
                    texto,
                    width=min(180, len(texto) * 5) # limita largura
                )
            ]
        )
        
class ContainerTarefas(ft.Container):
    def __init__(self, data, dados: list, pai):
        super().__init__()
        self.data = data
        self.dados = dados
        self.pai = pai  # armazenar main_page se precisar depois

        # Configuração visual
        self.padding = 15  
        self.aberto = False
        self.arrow = ArrowButton(self.expandir)
        self.arrow.rotate = 0

        # Cabeçalho com título e botão de expandir
        self.header = ft.Container(
            content=ft.Row(    
                controls=[
                    self.arrow,
                    ft.Text("Para " + self.data, size=18)
                ]
            ),
            padding=10,
            border=ft.border.only(bottom=ft.border.BorderSide(1, cores["fore2"]))
        )

        # Coluna com as tarefas (inicialmente invisível)
        self.tarefas = ft.Column(
            controls=[
                Tarefa(
                    tarefa['id'],
                    tarefa['id_pagina'],
                    tarefa['titulo'],
                    tarefa['data_de_criacao'],
                    self.pai,
                    self,
                    tarefa["finalizado"],
                    desc=tarefa['descricao'],
                    categoria=tarefa['categoria'],
                    prioridade=tarefa['prioridade'],
                    data_term=tarefa['data_de_termino'],
                )
                for tarefa in self.dados
            ],
            visible=False,
            expand=True,
            spacing=10
        )

        # Content é composto do cabeçalho + coluna de tarefas
        self.content = ft.Column(
            controls=[
                self.header,
                self.tarefas
            ],
            spacing=10
        )

    def expandir(self, e):
        self.aberto = not self.aberto
        self.tarefas.visible = self.aberto
        self.arrow.rotate = 3.14/2 if self.aberto else 0
        self.update()

class Tarefa(ft.Container):
    def __init__(self, id_tarefa, id_pagina, titulo, data_cri, main_page, container_tarefas, finalizado, desc="", categoria="", prioridade=0, data_term=""):
        super().__init__()
        self.id = id_tarefa
        self.id_pagina = id_pagina
        self.titulo = titulo
        self.desc = desc
        self.categoria = categoria
        self.prioridade = prioridade
        self.finalizado = finalizado
        self.data_criacao = data_cri
        self.data_termino = data_term

        self.padding = 20
        self.border_radius = 10
        self.bgcolor = cores["bg_tarefa"]

        # Parte interativa
        self.func = lambda e : print('teste')

        def apagar_info(info_tarefa): 
            main_page.content.controls.remove(info_tarefa)
            container_tarefas.tarefas.controls.remove(self)
            
            db.delete_tarefa(self.id)
            main_page.att_datas()
        self.apagar_info = apagar_info

        def apagar():
            container_tarefas.tarefas.controls.remove(self)
            db.delete_tarefa(self.id)
            container_tarefas.tarefas.update()
            main_page.att_datas()

        def salvar(info_tarefa):
            main_page.content.controls.remove(info_tarefa)
            db.edit_tarefa(info_tarefa.id, info_tarefa.titulo, info_tarefa.descricao, info_tarefa.prioridade, info_tarefa.data_termino)

            main_page.update()
        
        def editar():
            main_page.content.controls.append(
                InfoTarefa(
                    self.id,
                    self.titulo,
                    self.desc,
                    self.data_criacao,
                    self.data_termino,
                    self.prioridade,
                    self.categoria,
                    self.id_pagina,
                    apagar_info,
                    salvar,
                    main_page
                )
            )
            main_page.update()

        self.icons = ft.Row(
            controls=[
                MyIconBtn("src/assets/edit_icon.png", lambda e: editar(), 1),
                MyIconBtn("src/assets/remove_icon.png", lambda e: apagar(), 1)
            ]
        )

        # Conteudo
        self.content = ft.Row(
            controls=[
                ft.Checkbox(
                    label=self.titulo,
                    on_change=lambda e: db.check_tarefa(self.id),
                    value=True if self.finalizado else False
                )
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN
        )

        def hover(e):
            hovering = True if e.data == "true" else False
            
            if hovering:
                self.bgcolor = cores["bg_tarefa_hover"] 
                self.content.controls.append(self.icons)
            else:
                self.bgcolor = cores["bg_tarefa"]
                self.content.controls.remove(self.icons)
            
            self.update()
        
        self.on_hover = hover

# Componentes para a janela de detalhes da tarefa
class InfoTarefa(ft.Container):
    def __init__(self, id, titulo, descricao, data_cri, data_term, prio, categoria, id_pagina, rm_func, save_func, main_page):
        super().__init__()
        self.bgcolor = cores["bg2"]
        self.width = 800
        self.height = 500
        self.padding = 20

        # Dados
        self.id = id
        self.titulo = titulo
        self.descricao = descricao
        self.data_criacao = data_cri
        self.data_termino = data_term
        self.prioridade = prio
        self.categoria = categoria
        self.id_pagina = id_pagina

        self.save_fn = lambda e: save_func(self)
        self.rm_fn = lambda e: rm_func(self)
        def sair():
            main_page.content.controls.remove(self)
            main_page.update()

        def att_content(titulo='', desc='', term='', prio='', cat=''):
            if titulo:
                self.titulo = titulo
            if desc:
                self.descricao = desc
            if term:
                self.data_termino = term
            if prio:
                self.prioridade = prio
            if cat:
                self.categoria = cat

        self.content = ft.Stack(
            controls=[
                ft.Row( # Conteúdo
                    controls=[
                        ft.Container( # Parte da Esquerda
                            content=ft.Column(
                                controls=[
                                    ft.Column( # Detalhes da tarefa
                                        controls=[
                                            ft.Text("Data de Criação:", color=cores["fore1"], weight=ft.FontWeight.BOLD),
                                            LabelEditavel(
                                                self.data_criacao,
                                                "date",
                                            )
                                        ]
                                    ),
                                    ft.Column( # Detalhes da tarefa
                                        controls=[
                                            ft.Text("Data de término:", color=cores["fore1"], weight=ft.FontWeight.BOLD),
                                            LabelEditavel(
                                                self.data_termino,
                                                "date",
                                                on_submit=lambda value: att_content(term=value)
                                            )
                                        ]
                                    ),
                                    ft.Column( # Detalhes da tarefa
                                        controls=[
                                            ft.Text("Prioridade:", color=cores["fore1"], weight=ft.FontWeight.BOLD),
                                            LabelEditavel(
                                                self.prioridade,
                                                "int",
                                                on_submit=lambda value: att_content(prio=value)
                                            )
                                        ]
                                    ),
                                    ft.Column( # Detalhes da tarefa
                                        controls=[
                                            ft.Text("Categoria:", color=cores["fore1"], weight=ft.FontWeight.BOLD),
                                            LabelEditavel(
                                                self.categoria,
                                                "str",
                                                on_submit=lambda value: att_content(cat=value)
                                            )
                                        ]
                                    )
                                ],
                                expand=True
                            ),
                            bgcolor=cores["bg2"],
                            shadow=ft.BoxShadow(blur_radius=4, color=ft.Colors.BLACK, offset=ft.Offset(-4, 5)),
                            border_radius=10,
                            padding=10
                        ),
                        ft.Container( # Parte da direita
                            content=ft.Column(
                                controls=[
                                    LabelEditavel( # Titulo
                                        self.titulo,
                                        "str",
                                        scale=4,
                                        on_submit=lambda value: att_content(titulo=value)
                                    ),
                                    ft.Column( # Coluna para descrição
                                        controls=[
                                            ft.Text("Descrição:", size=25, color=cores["fore1"]),
                                            ft.Container(
                                                bgcolor=cores["bg1"],
                                                expand=True,
                                                width=float("inf"),
                                                content=LabelEditavel(
                                                    self.descricao,
                                                    "str",
                                                    on_submit=lambda value: att_content(desc=value)
                                                ),
                                            )
                                        ],
                                        expand=True
                                    ),
                                    ft.Row( # Row para os botões
                                        alignment=ft.MainAxisAlignment.END,
                                        spacing=30,
                                        controls=[
                                            ft.Button(
                                                "Excluir",
                                                bgcolor=cores["fore2"],
                                                color=cores["fore1"],
                                                on_click=self.rm_fn
                                            ),
                                            ft.Button(
                                                "Salvar",
                                                bgcolor=cores["fore2"], 
                                                color=cores["fore1"],
                                                on_click=self.save_fn
                                            )
                                        ]
                                    )
                                ],
                                spacing=40,
                                expand=True
                            ),
                            bgcolor=cores["bg2"],
                            shadow=ft.BoxShadow(blur_radius=4, color=ft.Colors.BLACK, offset=ft.Offset(-4, 5)),
                            expand=True,
                            border_radius=10,
                            padding=10
                        )
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_AROUND,
                    spacing=20
                ),
                ft.IconButton(
                    icon=ft.Icons.EXIT_TO_APP,
                    icon_color=cores["fore2"],
                    top=10,
                    right=10,
                    on_click=lambda e: sair()
                ),
            ]
        )

class LabelEditavel(ft.Container):
    def __init__(self, content, type, scale=1, on_submit=None):
        super().__init__()
        self.type = type
        self.content_value = str(content)
        self.on_submit = on_submit
        self.padding = 5
        self.border_radius = 6

        # Parte editável
        self.text = ft.Text(self.content_value, color=cores["fore1"], size=14*scale)  # Modo texto
        self.input = ft.TextField(value=self.content_value, autofocus=True, color=cores["fore1"], text_size=14*scale, width=100*scale)  # Modo editável

        # Eventos
        if on_submit:
            self.on_hover = self.hover

        self.on_click = self.edit
        self.input.on_submit = self.save
        self.input.on_blur = self.save

        # Inicializa com modo texto
        self.conteudo = ft.Column(controls=[self.text])
        self.content = self.conteudo 

    def hover(self, e):
        self.bgcolor = cores["bg_tarefa"] if e.data == "true" else ''
        self.update()

    def edit(self, e):
        self.input.value = self.content_value
        self.conteudo.controls = [self.input]  # Troca o modo visual para input
        self.update()
        self.input.focus()  # Precisa vir após o update

    def save(self, e):
        def data_valida(data_str):
            try:
                datetime.strptime(data_str, "%d/%m/%Y")
                return True
            except ValueError:
                try:
                    datetime.strptime(data_str, "%d-%m-%Y")
                    return True
                except ValueError:
                    return False
            

        valid = (
            (self.type == 'int' and self.input.value.isdigit()) or
            (self.type == 'date' and data_valida(self.input.value)) or
            self.type == "str"
        )

        if valid:
            self.content_value = self.input.value
            self.text.value = self.content_value
            if self.on_submit:
                self.on_submit(self.content_value)

        self.conteudo.controls = [self.text]  # Volta para o modo texto
        self.update()

class BotaoPagina(ft.Container):
    def __init__(self, fn, titulo, id, left_menu):
        super().__init__()
        self.on_click = fn
        self.id = id
        self.menu = left_menu

        self.bg_color = "#00000000"
        self.width = float("inf")
        self.padding = 5
        self.border_radius = 5
        self.margin = 10


        self.content = ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            controls=[
                ft.Text(titulo)
            ]
        )

        def on_hover(e):
            hovering = True if e.data == "true" else False

            if hovering:
                self.bgcolor = cores["bg_tarefa"]
                self.content.controls.append(
                    ft.IconButton(
                        icon=ft.Icons.CLOSE,
                        on_click=lambda e: self.delete(self.id)
                    )
                )
            else:
                self.bgcolor ="#00000000"
                self.content.controls.pop()

            self.update()

        self.on_hover = on_hover

    def delete(self, id):
        db.delete_pagina(id)

        self.menu.att_paginas()
        

