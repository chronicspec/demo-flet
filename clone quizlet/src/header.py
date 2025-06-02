import flet as ft
import constant

def app_header(title=None, show_back=False, on_back=None):
    return ft.Container(
        ft.Row(
            [
                ft.IconButton(
                    icon=ft.Icons.ARROW_BACK,
                    on_click=on_back
                ) if show_back else ft.Container(width=40),
                ft.Text(title or constant.HEADER_TEXT, size=20, weight=ft.FontWeight.BOLD),
            ],
            alignment=ft.MainAxisAlignment.START,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        bgcolor=ft.Colors.BLUE_100,
        padding=10,
    )