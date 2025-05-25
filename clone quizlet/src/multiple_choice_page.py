import flet as ft
import constant

class MultipleChoiceApp:
    def __init__(self, flashcards):
        self.flashcards = flashcards
        self.index = 0
        self.correct_definition = ""
        self.feedback = ft.Text(size=18, weight=ft.FontWeight.BOLD)
        self.question_text = ft.Text(value="", size=30, weight=ft.FontWeight.BOLD)

        self.buttons = [
            ft.ElevatedButton(text="...", width=400, on_click=self.check_answer)
            for _ in range(4)
        ]

        self.next_button = ft.ElevatedButton(
            text="Tiếp", on_click=self.next_question, visible=False
        )

        self.layout = ft.Column([
            self.question_text,
            *self.buttons,
            self.feedback,
            self.next_button,
            ft.ElevatedButton(text="Tiếp", on_click=self.next_question, visible=False)
        ])
        self.load_question()

    def load_question(self):
        # Xử lý hiển thị câu hỏi mới ở đây
        pass

    def check_answer(self, e):
        # Xử lý kiểm tra đáp án ở đây
        pass

    def next_question(self, e):
        # Xử lý chuyển sang câu hỏi tiếp theo ở đây
        pass
