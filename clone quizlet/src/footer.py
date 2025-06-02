import flet as ft
import constant

def app_footer():
    return ft.Container(
        ft.Text(constant.FOOTER_TEXT, size=12, color=ft.Colors.GREY),
        alignment=ft.alignment.center,
        padding=10,
    )