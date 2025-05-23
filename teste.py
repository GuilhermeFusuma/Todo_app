import flet as ft
from datetime import datetime

class EditableLabel(ft.Container):
    def __init__(self, titulo, content, type, on_submit=None):
        super().__init__()
        self.titulo = titulo
        self.type = type
        self.content_value = content
        self.on_submit = on_submit
        self.width = 170

        # Parte editavel
        self.text = ft.Text(self.content_value) # Modo texto
        self.input = ft.TextField(value=self.content_value, autofocus=True, max_length=60) # Modo editável
        self.editavel = ft.Container(controls=[self.text])

        # Eventos
        self.on_click = self.edit

        self.input.on_submit = self.save # salva ao enviar
        self.input.on_blur = self.save # Salva quando clica fora

        self.content = ft.Column( # Inicializa com o texto
            controls=[
                ft.Text(self.titulo),
                self.editavel
            ]
        )

    def edit(self, e):
        self.input.value = self.content_value
        self.editavel = self.input
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
        if self.on_submit and valid:
            self.on_submit(self.content_value)


    

def main(page: ft.Page):
    def ao_salvar(novo_texto):
        print("Novo valor:", novo_texto)

    page.add(EditableLabel("Clique para editar", "int", on_submit=ao_salvar))

ft.app(target=main)