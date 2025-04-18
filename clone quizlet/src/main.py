import flet as ft
import json
import os
import random

# --- Flashcard class ---
class Flashcard:
    def __init__(self, question, answer):
        self.question = question
        self.answer = answer

    def to_dict(self):
        return {"question": self.question, "answer": self.answer}

    @staticmethod
    def from_dict(data):
        return Flashcard(data["question"], data["answer"])

# --- Load flashcards from .txt file ---
def load_flashcards_from_txt_file(filename):
    flashcards = []
    if not filename:
        return flashcards
    if os.path.exists(filename):
        with open(filename, "r", encoding="utf-8") as f:
            for line in f:
                if ":" in line:
                    question, answer = line.strip().split(":", 1)
                    flashcards.append(Flashcard(question.strip(), answer.strip()))
    return flashcards

# --- Save flashcards thủ công ---
FLASHCARD_JSON = "flashcards.json"

def save_flashcards(flashcards):
    with open(FLASHCARD_JSON, "w", encoding="utf-8") as f:
        json.dump([card.to_dict() for card in flashcards], f, ensure_ascii=False, indent=2)

def load_flashcards_from_json():
    if os.path.exists(FLASHCARD_JSON):
        with open(FLASHCARD_JSON, "r", encoding="utf-8") as f:
            data = json.load(f)
            return [Flashcard.from_dict(item) for item in data]
    return []

# --- Main App ---
def main(page: ft.Page):
    page.title = "Learn Flashcards ✍️"
    page.theme_mode = "light"
    page.vertical_alignment = "center"
    page.horizontal_alignment = "center"
    page.padding = 30

    flashcards = []
    learn_list = []
    current_card = None
    answer_correct = 0
    answer_wrong = 0

    input_answer = ft.TextField(label="Nhập đáp án", border="outline", expand=True)
    feedback_text = ft.Text(size=16, weight="bold")
    progress_text = ft.Text(size=14)
    card_display = ft.Text("🎓 Bấm 'Bắt đầu học' để luyện tập", size=20, weight="bold", text_align="center")

    # --- Banner setup ---
    banner = ft.Banner(
        content=ft.Text(""),
        bgcolor=ft.colors.BLUE_100,
        leading=ft.Icon(ft.icons.INFO, color=ft.colors.BLUE),
        actions=[ft.TextButton("Đóng", on_click=lambda e: close_banner())],
        visible=False
    )

    def show_banner(message: str, color=ft.colors.BLUE_100):
        banner.content.value = message
        banner.bgcolor = color
        banner.visible = True
        page.update()

    def close_banner():
        banner.visible = False
        page.update()

    page.banner = banner

    # --- File Picker setup ---
    file_picker = ft.FilePicker()

    def on_file_picked(e: ft.FilePickerResultEvent):
        nonlocal flashcards
        if e.files and e.files[0].path:
            filepath = e.files[0].path
            flashcards = load_flashcards_from_txt_file(filepath)
            filename = os.path.basename(filepath)
            show_banner(f"✅ Đã load: {filename}", ft.colors.GREEN_100)
        else:
            show_banner("⚠️ Không chọn được file hợp lệ.", ft.colors.RED_100)

    file_picker.on_result = on_file_picked
    page.overlay.append(file_picker)

    # --- Học flashcards ---
    def start_learning(e):
        nonlocal learn_list, answer_correct, answer_wrong
        if not flashcards:
            show_banner("❗ Chưa có thẻ để học.", ft.colors.RED_100)
            return
        learn_list = flashcards.copy()
        random.shuffle(learn_list)
        answer_correct = 0
        answer_wrong = 0
        next_card()

    def next_card():
        nonlocal current_card
        if not learn_list:
            card_display.value = "🎉 Bạn đã hoàn thành tất cả thẻ!"
            feedback_text.value = f"✅ Đúng: {answer_correct} | ❌ Sai: {answer_wrong}"
            input_answer.visible = False
            check_button.visible = False
            page.update()
            return

        current_card = learn_list[0]
        card_display.value = current_card.question
        input_answer.value = ""
        input_answer.visible = True
        check_button.visible = True
        feedback_text.value = ""
        progress_text.value = f"📚 Còn lại: {len(learn_list)} thẻ"
        page.update()

    def check_answer(e):
        nonlocal answer_correct, answer_wrong
        if not current_card:
            return
        user_input = input_answer.value.strip().lower()
        correct = current_card.answer.strip().lower()
        if user_input == correct:
            feedback_text.value = "✅ Chính xác!"
            answer_correct += 1
            learn_list.pop(0)
        else:
            feedback_text.value = f"❌ Sai! Đáp án đúng: {current_card.answer}"
            answer_wrong += 1
            learn_list.append(learn_list.pop(0))
        next_card()

    # --- Thêm flashcard thủ công ---
    question_input = ft.TextField(label="Câu hỏi", width=200)
    answer_input = ft.TextField(label="Đáp án", width=200)

    def add_card(e):
        if question_input.value and answer_input.value:
            new_card = Flashcard(question_input.value, answer_input.value)
            flashcards.append(new_card)
            save_flashcards(flashcards)
            question_input.value = ""
            answer_input.value = ""
            show_banner("📥 Đã thêm thẻ mới!", ft.colors.GREEN_100)
            page.update()
        else:
            show_banner("⚠️ Vui lòng nhập đầy đủ câu hỏi và đáp án.", ft.colors.RED_100)

    check_button = ft.ElevatedButton("💡 Kiểm tra", on_click=check_answer, bgcolor="#007bff", color="white")

    # --- Giao diện ---
    page.add(
        banner,
        ft.Column([
            ft.Text("🧠 Flashcard - Chế độ Learn", size=28, weight="bold", text_align="center"),
            ft.Divider(),

            ft.Row([
                question_input,
                answer_input,
                ft.ElevatedButton("➕ Thêm thẻ", on_click=add_card),
            ], alignment="center"),

            ft.ElevatedButton("📂 Chọn file flashcard (.txt) từ máy", on_click=lambda e: file_picker.pick_files(allow_multiple=False)),

            ft.Divider(),

            ft.Container(
                content=ft.Card(
                    ft.Container(
                        content=card_display,
                        padding=20,
                        alignment=ft.alignment.center,s
                    )
                ),
                alignment=ft.alignment.center,
                width=500
            ),

            ft.Row([input_answer, check_button], alignment="center"),
            feedback_text,
            progress_text,

            ft.ElevatedButton("🚀 Bắt đầu học", on_click=start_learning, bgcolor="green", color="white")
        ], spacing=20, alignment="center")
    )

ft.app(target=main)
