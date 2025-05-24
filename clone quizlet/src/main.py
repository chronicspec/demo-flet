import flet as ft
from flashcard_page import FlashcardPage
from multiple_choice_page import MultipleChoiceApp
import constant
import asyncio


def main(page: ft.Page):
    page.title = constant.APP_TITLE

    selected_flashcards = []

    # File picker
    file_picker = ft.FilePicker(on_result=lambda e: asyncio.create_task(file_picker_result_async(e, page)))
    page.overlay.append(file_picker)

    def open_file_picker(e):
        file_picker.pick_files(allow_multiple=False)

    # Các nút disabled ban đầu
    flashcard_btn = ft.ElevatedButton(text="📘 Học Flashcard", disabled=True)
    quiz_btn = ft.ElevatedButton(text="🎯 Làm Trắc nghiệm", disabled=True)

    async def file_picker_result_async(e: ft.FilePickerResultEvent, page: ft.Page):
        if e.files:
            f = e.files[0]
            bytes_data = await f.read()
            content = bytes_data.decode("utf-8")
            flashcards = parse_flashcards_from_txt(content)

            if len(flashcards) < 1:
                page.snack_bar = ft.SnackBar(ft.Text("File không có dữ liệu flashcard hợp lệ!"))
                page.snack_bar.open = True
                page.update()
                return

            selected_flashcards.clear()
            selected_flashcards.extend(flashcards)
            flashcard_btn.disabled = False
            quiz_btn.disabled = False
            page.update()

    def parse_flashcards_from_txt(text: str):
        flashcards = []
        for line in text.splitlines():
            line = line.strip()
            if not line or "|" not in line:
                continue
            term, definition = line.split("|", 1)
            flashcards.append({"term": term.strip(), "definition": definition.strip()})
        return flashcards

    def go_to_flashcard(e):
        flashcard_view = FlashcardPage(selected_flashcards)
        page.views.append(
            ft.View(
                "/flashcard",
                [flashcard_view.layout],
                appbar=ft.AppBar(title=ft.Text("📘 Flashcard")),
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
                [quiz_view.layout],
                appbar=ft.AppBar(title=ft.Text("🎯 Trắc nghiệm")),
                vertical_alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            )
        )
        page.go("/quiz")

    flashcard_btn.on_click = go_to_flashcard
    quiz_btn.on_click = go_to_quiz

    page.add(
        ft.Column(
            [
                ft.Text(constant.APP_TITLE, size=40, weight=ft.FontWeight.BOLD),
                ft.ElevatedButton(text="Chọn file .txt chứa bộ câu hỏi", on_click=open_file_picker),
                flashcard_btn,
                quiz_btn,
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=30,
        )
    )


ft.app(target=main)
