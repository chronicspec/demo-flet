import flet as ft
from flashcard_page import FlashcardPage
from multiple_choice_page import MultipleChoiceApp
import constant
from file_upload import FileUpload
from header import app_header
from footer import app_footer

selected_flashcards = []

def main(page: ft.Page):
    page.title = constant.APP_TITLE

    flashcard_btn = ft.ElevatedButton("Flashcard", disabled=True)
    quiz_btn = ft.ElevatedButton("Quiz", disabled=True)

    async def on_upload_success(flashcards):
        selected_flashcards.clear()
        selected_flashcards.extend(flashcards)
        flashcard_btn.disabled = False
        quiz_btn.disabled = False
        page.snack_bar = ft.SnackBar(ft.Text(f"✅ Đã nạp {len(flashcards)} flashcard thành công!"))
        page.snack_bar.open = True
        page.update()

    file_upload_widget, file_picker = FileUpload(on_upload_success)
    page.overlay.append(file_picker)

    def go_to_flashcard(e):
        flashcard_view = FlashcardPage(selected_flashcards)
        page.views.append(
            ft.View(
                "/flashcard",
                [
                    app_header("📘 Flashcard", show_back=True, on_back=lambda e: page.go("/")),
                    flashcard_view.layout,
                    app_footer()
                ],
                vertical_alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            )
        )
        page.go("/flashcard")

    def go_to_quiz(e):
        quiz_view = MultipleChoiceApp(selected_flashcards)
        page.views.append(
            ft.View(
                "/quiz",
                [
                    app_header("🎯 Trắc nghiệm", show_back=True, on_back=lambda e: page.go("/")),
                    quiz_view.layout,
                    app_footer()
                ],
                vertical_alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            )
        )
        page.go("/quiz")

    flashcard_btn.on_click = go_to_flashcard
    quiz_btn.on_click = go_to_quiz

    def on_route_change(e):
        if len(page.views) > 1:
            page.views.pop()
        page.update()

    page.on_route_change = on_route_change

    page.add(
        ft.Column(
            [
                app_header(),
                file_upload_widget,
                flashcard_btn,
                quiz_btn,
                app_footer(),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20
        )
    )

ft.app(target=main)
