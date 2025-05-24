import flet as ft

class FlashcardPage:
    def __init__(self, flashcards):
        self.flashcards = flashcards
        self.index = 0

        self.term = ft.Text(size=30, weight=ft.FontWeight.BOLD)
        self.definition = ft.Text(size=24)
        self.next_btn = ft.ElevatedButton(text="Tiếp", on_click=self.next_card)

        self.layout = ft.Column(
            [
                self.term,
                self.definition,
                self.next_btn,
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20,
        )

        self.load_card()

    def load_card(self):
        flashcard = self.flashcards[self.index]
        self.term.value = flashcard["term"]
        self.definition.value = flashcard["definition"]

    def next_card(self, e):
        self.index = (self.index + 1) % len(self.flashcards)
        self.load_card()
        self.layout.update()
