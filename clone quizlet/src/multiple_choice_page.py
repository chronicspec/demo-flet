import flet as ft
import random
import asyncio
import constant

class MultipleChoiceApp:
    def __init__(self, flashcards):
        self.flashcards = flashcards
        self.current_index = 0
        self.score = 0

        self.question_text = ft.Text(size=20, weight="bold")
        self.feedback = ft.Text(size=16)
        self.buttons = [
            ft.ElevatedButton(text="...", width=400, on_click=self.check_answer)
            for _ in range(4)
        ]
        self.next_button = ft.ElevatedButton(
            text=constant.MC_NEXT, on_click=self.next_question, visible=False
        )

        self.layout = ft.Column(
            [
                self.question_text,
                *self.buttons,
                self.feedback,
                self.next_button,
            ],
            alignment=ft.MainAxisAlignment.START,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=10,
        )

        self.load_question()

    def load_question(self):
        if self.current_index >= len(self.flashcards):
            self.question_text.value = constant.MC_DONE.format(
                score=self.score, total=len(self.flashcards)
            )
            for btn in self.buttons:
                btn.visible = False
            self.feedback.value = ""
            self.next_button.visible = False
            return

        self.feedback.value = ""
        self.next_button.visible = False

        # Lấy câu hỏi hiện tại
        current = self.flashcards[self.current_index]
        self.question_text.value = constant.MC_QUESTION.format(
            index=self.current_index + 1, question=current['term']
        )

        # Tạo danh sách đáp án (1 đúng, 3 sai)
        answers = [current["definition"]]
        wrong_answers = [fc["definition"] for i, fc in enumerate(self.flashcards) if i != self.current_index]
        answers += random.sample(wrong_answers, min(3, len(wrong_answers)))
        random.shuffle(answers)

        # Gán text cho các nút
        for i, btn in enumerate(self.buttons):
            if i < len(answers):
                btn.text = answers[i]
                btn.visible = True
                btn.disabled = False
            else:
                btn.visible = False

        self.correct_answer = current["definition"]

    def check_answer(self, e):
        selected = e.control.text
        for btn in self.buttons:
            btn.disabled = True
        if selected == self.correct_answer:
            self.score += 1
            self.feedback.value = constant.MC_CORRECT
            self.layout.update()
            e.page.run_task(self.auto_next)
        else:
            self.feedback.value = constant.MC_WRONG.format(answer=self.correct_answer)
            self.next_button.visible = True
            self.layout.update()

    async def auto_next(self):
        await asyncio.sleep(1)
        self.current_index += 1
        self.load_question()
        self.layout.update()

    def next_question(self, e):
        self.current_index += 1
        self.load_question()
        self.layout.update()
