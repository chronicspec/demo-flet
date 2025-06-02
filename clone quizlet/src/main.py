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

    flashcard_btn = ft.ElevatedButton(constant.BTN_FLASHCARD, disabled=True)
    quiz_btn = ft.ElevatedButton(constant.BTN_QUIZ, disabled=True)

    async def on_upload_success(flashcards):
        selected_flashcards.clear()
        selected_flashcards.extend(flashcards)
        flashcard_btn.disabled = False
        quiz_btn.disabled = False
        page.snack_bar = ft.SnackBar(ft.Text(constant.UPLOAD_SUCCESS.format(count=len(flashcards))))
        page.snack_bar.open = True
        page.update()

    file_upload_widget, file_picker = FileUpload(on_upload_success)
    page.overlay.append(file_picker)

    def go_to_flashcard(e):
        if not any(v.route == "/flashcard" for v in page.views):
            flashcard_view = FlashcardPage(selected_flashcards)
            page.views.append(
                ft.View(
                    "/flashcard",
                    [
                        app_header(constant.FLASHCARD_HEADER, show_back=True, on_back=lambda e: page.go("/")),
                        flashcard_view.layout,
                        app_footer()
                    ],
                    vertical_alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                )
            )
        page.go("/flashcard")

    def go_to_quiz(e):
        if not any(v.route == "/quiz" for v in page.views):
            quiz_view = MultipleChoiceApp(selected_flashcards)
            page.views.append(
                ft.View(
                    "/quiz",
                    [
                        app_header(constant.QUIZ_HEADER, show_back=True, on_back=lambda e: page.go("/")),
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
        app_header(),
        ft.Column(
            [
                file_upload_widget,
                flashcard_btn,
                quiz_btn,
                app_footer(),
            ],
            alignment=ft.MainAxisAlignment.START,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20
        )
    )

ft.app(target=main)
