import flet as ft

def FileUpload(on_upload_success):
    file_picker = ft.FilePicker()
  
    async def file_picker_result(e: ft.FilePickerResultEvent):

        if e.files:
            f = e.files[0]
            if hasattr(f, "content") and f.content is not None:
                content = f.content.decode("utf-8")
            elif hasattr(f, "path") and f.path is not None:
                with open(f.path, "r", encoding="utf-8") as file:
                    content = file.read()
            else:
                ft.snack_bar = ft.SnackBar(ft.Text("⚠️ Không đọc được file!"))
                ft.snack_bar.open = True
                return

            # Parse flashcards
            flashcards = []
            lines = content.strip().split("\n")
            for line in lines:
                parts = line.split("|")
                if len(parts) == 2:
                    question = parts[0].strip()
                    answer = parts[1].strip()
                    flashcards.append({"term": question, "definition": answer})

            if not flashcards:
                ft.snack_bar = ft.SnackBar(ft.Text("⚠️ File không hợp lệ hoặc trống"))
                ft.snack_bar.open = True
                return

            # Gọi callback
            await on_upload_success(flashcards)
        else:
            ft.snack_bar = ft.SnackBar(ft.Text("⚠️No files selected"))
            ft.snack_bar.open = True
            return

    file_picker.on_result = file_picker_result

    def open_file_dialog(e):
        print("Opening file dialog")
        file_picker.pick_files(allow_multiple=False)

    return ft.Column(
        [
            ft.Text("📂 Chọn file bộ câu hỏi (.txt, dạng: question|answer)"),
            ft.ElevatedButton("Chọn file", on_click=open_file_dialog),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=20
    ), file_picker