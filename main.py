import flet as ft
import os

for file in range(476):
    os.rename(f"Definite_German_Articles/{file}", f"Definite_German_Articles/{file}.jpg")

""" 
import flet as ft

def main(page: ft.Page):
    
    text: ft.Container = ft.Container(
        border = ft.border.all(1, "#FFFF00"),
        expand = True,
        content = ft.Text(
            "Hola Paty",
            font_family = "Verdana",
            font_size = 35,
            font_color = "#FFFF00"
        )
    )

    page.add(
        ft.Column(
            controls = [
                text
            ]
        )
    )

    page.update()


if __name__ == "__main__":
    ft.app(target = main, view = ft.AppView.WEB_BROWSER)
     """