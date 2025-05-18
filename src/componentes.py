import flet as ft
from cores import cores

# botão flecha que executa uma função passada nos argumentos
class ArrowButton(ft.IconButton):
    def __init__(self, func):
        super().__init__()
        self.icon = ft.Icons.ARROW_CIRCLE_LEFT
        self.icon_color = cores["fore1"]
        self.icon_size = 20

        self.on_click = func

# Balão para o chat
class Balao(ft.Row):
    def __init__(self, texto, agente="user"):
        super().__init__()
        self.expand = True
        self.alignment = ft.alignment.center_right
        self.padding = 30

        self.controls = [
            ft.Container(
                content = ft.Column(
                    controls=self.wrap_text(texto)
                ),
                bgcolor = cores["bg2"],
                padding = 10,
            )
        ]

    #TODO fazer a função retornar uma lista de textos que não passam do tamanho do chat
    def wrap_text(self, text):
        linhas = []
        # Temporário apenas para não quebrar o app
        linhas.append(ft.Text(text))

        return linhas