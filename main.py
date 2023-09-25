
import flet as ft

def main(page: ft.Page):

    english_txt: ft.Text = ft.Text(
        "Cabinet / Cupboard",
        size = 35,
        font_family = "Open Sans",
        color = "#FFFFFF"
    )

    german_txt: ft.Text = ft.Text(
        "Der Schrank",
        size = 35,
        font_family = "Open Sans",
        color = "#FFDD1C"
    )

    img: ft.Image = ft.Image(
        src = "DerSchrank.jpg"
    )

    flashcard: ft.Container = ft.Container(
        width = 700,
        height = 500,
        border_radius = ft.border_radius.all(25),
        bgcolor = "#38352C",
        content = ft.Column(
            alignment = ft.MainAxisAlignment.CENTER,
            controls = [
                ft.Row(
                    alignment = ft.MainAxisAlignment.CENTER,
                    controls = [
                        img
                    ]
                ),
                ft.Row(
                    alignment = ft.MainAxisAlignment.CENTER,
                    controls = [
                        german_txt
                    ]
                ),
                ft.Row(
                    alignment = ft.MainAxisAlignment.CENTER,
                    controls = [
                        english_txt
                    ]
                )
            ]
        )
    )

    page.add(flashcard)

    page.update()


if __name__ == "__main__":
    ft.app(target = main, assets_dir = "assets")
