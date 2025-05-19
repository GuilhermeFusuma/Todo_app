import flet as ft
from cores import cores

# botão flecha que executa uma função passada nos argumentos
class ArrowButton(ft.IconButton):
    def __init__(self, func):
        super().__init__()
        self.icon = ft.Icons.ARROW_FORWARD_IOS
        self.icon_color = cores["fore1"]
        self.icon_size = 20

        self.on_click = func

# Balão para o chat
class Balao(ft.Container):
    def __init__(self, texto, agente="user"):
        super().__init__()

        self.bgcolor = cores["bg2"]
        self.padding = 10
        self.border_radius = 10
        self.max_width = 200  # limita largura
        self.content = ft.Column(
            controls=self.wrap_text(texto)
        )

    #TODO fazer a função retornar uma lista de textos que não passam do tamanho do chat
    def wrap_text(self, text):
        linhas = []
        # Temporário apenas para não quebrar o app
        linhas.append(ft.Text(text))

        return linhas

class Tarefa(ft.Container):
    def __init__(self, id_tarefa, desc="", data_term=""):
        super().__init__()
        self.id = id_tarefa

        # detalhes = 

        self.padding = 20
        self.width = float("inf")
        self.bgcolor = cores["bg_tarefa"]

        self.content = ft.Text("isso é um teste")

# class TarefaDetalhes(ft.Container):
#     def __init__(self, )

class ContainerTarefas(ft.Container):
    def __init__(self, data, dados="todo"):
        #TODO pensar em uma forma de pegar os dados de uma forma que eu possa separar de forma eficiente 
        super().__init__()
        self.data = data

        # Config
        self.padding = 15
        self.expand = True
        
        self.aberto = False
        self.arrow = ArrowButton(self.expandir)
        self.arrow.rotate = 0 

        self.header = ft.Container(
            content=ft.Row(    
                controls=[
                    self.arrow,
                    ft.Text(self.data, size=18)
                ]
            ),
            padding = 10,
            border=ft.border.only(bottom=ft.border.BorderSide(1, cores["fore2"]))
        )

        self.tarefas = [
            Tarefa(1),
            Tarefa(2)
        ]

        self.content = ft.Column(
            controls=[
                self.header
            ],
            spacing=20
        )

    def expandir(self, e):
        if not self.aberto:
            for tarefa in self.tarefas:
                self.content.controls.append(tarefa)
            self.arrow.rotate = 3.14/2 # Rotaciona para baixo
            self.aberto = True

        elif self.aberto:
            self.content.controls = [self.header] # remove as tarefas deixando apenas o header
            self.header
            self.aberto = False
            self.arrow.rotate = 0

        self.update()