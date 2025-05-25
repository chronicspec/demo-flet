import flet as ft

def app_footer():
    return ft.Container(
        ft.Text("© 2025 Quizlet Clone - Powered by Flet", size=12, color=ft.Colors.GREY),
        alignment=ft.alignment.center,
        padding=10,
    )