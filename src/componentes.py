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
        
class Tarefa(ft.Container):
    def __init__(self, id_tarefa, titulo, data_cri, desc="", categoria="", prioridade=0, data_term=""):
        super().__init__()
        self.id = id_tarefa
        self.titulo = titulo
        self.desc = desc
        self.categoria = categoria
        self.prioridade = prioridade
        self.data_criacao = data_cri
        self.data_termino = data_term

        self.padding = 20
        self.border_radius = 10
        self.bgcolor = cores["bg_tarefa"]

        # Parte interativa
        self.func = lambda e : print('teste')

        def apagar(e): 
            db.delete_tarefa(self.id)
            self.update()

        self.apagar = apagar 
        
        # def editar(e):

        self.icons = ft.Row(
            controls=[
                MyIconBtn("src/assets/edit_icon.png", self.func, 1),
                MyIconBtn("src/assets/remove_icon.png", self.apagar, 1)
            ]
        )

        # Conteudo
        self.content = ft.Row(
            controls=[
                ft.Checkbox(label=self.titulo)
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

class TarefaDetalhes(ft.Container):
    def __init__(self):
        super().__init__()

# Componentes para a janela de detalhes da tarefa
class InfoTarefa(ft.Container):
    def __init__(self, info):
        

class LabelEditavel(ft.Container):
    def __init__(self, content, type, on_submit=None):
        super().__init__()
        self.type = type
        self.content_value = content
        self.on_submit = on_submit
        self.width = 170

        self.text = ft.Text(self.content_value) # Modo texto
        self.input = ft.TextField(value=self.content_value, autofocus=True, max_length=60) # Modo editável

        # Eventos
        self.on_click = self.edit

        self.input.on_submit = self.save # salva ao enviar
        self.input.on_blur = self.save # Salva quando clica fora

        self.content = self.text # Inicializa com o texto

    def edit(self, e):
        self.input.value = self.content_value
        self.content = self.input
        self.update()
        self.input.focus() # É necessário estar depois do update

    def save(self, e):
        valid = False

        def data_valida(data_str): 
            try:
                datetime.strptime(data_str, "%d/%m/%Y")
                return True
            except ValueError:
                return False

        # teste para checar se o valor é válido
        if self.type == 'int' and self.input.value.isdigit() or self.type == 'date' and data_valida(self.input.value):
            valid = True

        if valid:
            self.content_value = self.input.value
            self.text.value = self.content_value
            self.content = self.text
            self.update()
            if self.on_submit:
                self.on_submit(self.content_value)


class ContainerTarefas(ft.Container):

    def __init__(self, data, dados: list):
        #TODO pensar em uma forma de pegar os dados de uma forma que eu possa separar de forma eficiente 
        super().__init__()
        self.data = data

        self.dados = dados
        self.tarefas = ft.Column(expand=True)

        # Config
        self.padding = 15  
        
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

        # Adiciona as tarefas em classes no self.tarefas
        for tarefa in self.dados:
            self.tarefas.controls.append(
                Tarefa(
                    tarefa['id'],
                    tarefa['titulo'],
                    tarefa['data_de_criacao'],
                    tarefa['descricao'],
                    tarefa['categoria'],
                    tarefa['prioridade'],
                    tarefa['data_de_termino']
                )
            )

        self.content = ft.Column(
            controls=[
                self.header
            ],
            spacing=20
        )

    def expandir(self, e):
        if not self.aberto:
            for tarefa in self.tarefas.controls:
                self.content.controls.append(tarefa)
            self.arrow.rotate = 3.14/2 # Rotaciona para baixo
            self.aberto = True

        elif self.aberto:
            self.content.controls = [self.header] # remove as tarefas deixando apenas o header
            self.header
            self.aberto = False
            self.arrow.rotate = 0

        self.update()

class BotaoPagina(ft.Container):
    def __init__(self, fn, titulo):
        super().__init__()
        self.on_click = fn

        self.bg_color = "#00000000"
        self.width = float("inf")
        self.padding = 5
        self.border_radius = 5
        self.margin = 10

        self.content = ft.Text(titulo)

        def on_hover(e):
            self.bgcolor = cores["bg_tarefa"] if e.data == "true" else "#00000000"
            self.update()
            
        self.on_hover = on_hover


